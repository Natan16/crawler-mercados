import json
import re
from decimal import Decimal as D
from functools import partial
from urllib.parse import parse_qs, urlparse

import scrapy
from scrapy.shell import inspect_response

from core.models import Crawl, Mercado, Produto, ProdutoCrawl
from crawlers.items import PaoDeAcucarItem

header = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://www.paodeacucar.com",
    "referer": "https://www.paodeacucar.com/",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}


class PaoDeAcucarSpider(scrapy.Spider):
    name = "pao_de_acucar"

    custom_settings = {"ITEM_PIPELINES": {"crawlers.pipelines.PaoDeAcucarPipeline": 300}}

    def __init__(self, filial=461):
        self.filial = filial
        self.mercado = Mercado.objects.get(rede="PAO_DE_ACUCAR", filial=filial)
        self.crawl = Crawl.objects.create(mercado=self.mercado)
        self.produtos_map = {}

    def start_requests(self):
        departamentos = [
            "limpeza",
            "alimentos",
            "beleza-e-perfumaria",
            "bebidas",
            "bebidas-alcoolicas",
            "bebes-e-criancas",
            "cuidados-pessoais",
            "suplementos-alimentares",
            "eventos-e-festas",
            "utensilios-descartaveis",
            "petshop",
            "floricultura-e-jardim",
            "esporte-e-lazer",
            "cuidados-com-a-saude",
            "moveis-e-decoracao",
            "cama-mesa-e-banho",
            "papelaria",
            "brinquedos-e-jogos",
            "automotivos",
            "casa-e-construcao",
            "celulares-e-smartphones",
            "climatizacao-e-ventilacao",
            "eletrodomesticos",
            "eletroportateis",
            "games-e-videogames",
            "informatica",
            "moda",
        ]
        for departamento in departamentos:
            url = "https://api.linximpulse.com/engage/search/v3/navigates?apiKey=paodeacucar&origin=https://www.paodeacucar.com&page=1&resultsPerPage=100&multicategory={departamento}&salesChannel={filial}&salesChannel=catalogmkp&sortby=relevance"
            parse_first_dep = partial(self.parse_first, departamento=departamento)
            yield scrapy.Request(
                url.format(filial=self.filial, departamento=departamento), callback=parse_first_dep, headers=header
            )

    def parse(self, response, departamento):
        parsed_response = json.loads(response.text)
        # inspect_response(response, self)
        products = parsed_response["products"]
        for product in products:
            codigo_de_barras = product["details"].get("EAN1", [None])[0] or f"pao-de-acucar-{product['id']}"
            preco = product["price"]
            if product["status"] != "AVAILABLE":
                continue
            yield PaoDeAcucarItem(
                item=codigo_de_barras,
                nome=product["name"],
                categoria=product["categories"][0]["name"],
                departamento=departamento,
                preco=preco,
            )

    def parse_first(self, response, departamento):
        parsed_response = json.loads(response.text)
        link_last_page = parsed_response["pagination"]["last"]
        parsed_url = urlparse(link_last_page)
        num_pages = int(parse_qs(parsed_url.query)["page"][0])
        url = "https://api.linximpulse.com/engage/search/v3/navigates?apiKey=paodeacucar&origin=https://www.paodeacucar.com&page={page}&resultsPerPage=100&multicategory={departamento}&salesChannel={filial}&salesChannel=catalogmkp&sortby=relevance"
        for page in range(1, num_pages):
            parse_dep = partial(self.parse, departamento=departamento)
            yield scrapy.Request(
                url.format(filial=self.filial, departamento=departamento, page=page + 1),
                callback=parse_dep,
                headers=header,
            )

    def armazena_no_banco(self):
        produtos_a_criar = []
        produtos_crawl = []
        produtos_map = self.produtos_map
        produtos_existentes = Produto.objects.filter(item__in=produtos_map.keys()).in_bulk(field_name="item")
        for item, values in produtos_map.items():
            if item not in produtos_existentes:
                produto, _ = values

                match = re.search(r"[0-9]+,{0,1}[0-9]*[g|kg|l|ml]", item)
                if match:
                    quant = match.group().replace(",", ".")
                    if quant[-2:] == "ml":
                        produto.volume_ml = quant[:-2]
                    elif quant[-2:] == "kg":
                        produto.peso_liquido = 1000 * D(quant[:-2])
                        produto.peso_bruto = 1000 * D(quant[:-2])
                    elif quant[-1:] == "l":
                        produto.volume_ml = 1000 * D(quant[:-1])
                    else:
                        produto.peso_liquido = quant[:-1]
                        produto.peso_bruto = quant[:-1]
                produtos_a_criar.append(produto)

        produtos_criados = Produto.objects.bulk_create(produtos_a_criar, batch_size=1000)
        for p in produtos_criados:
            produtos_existentes[p.item] = p

        for codigo_de_barras, values in produtos_map.items():
            _, str_preco = values

            produtos_crawl.append(
                ProdutoCrawl(preco=D(str_preco), crawl=self.crawl, produto=produtos_existentes[codigo_de_barras])
            )
        ProdutoCrawl.objects.bulk_create(produtos_crawl, batch_size=1000)
