# https://api.spanionline.com.br/v1/loja/classificacoes_mercadologicas/secoes/75/produtos/filial/1/centro_distribuicao/10/ativos?orderby=produto.descricao:asc


import json
from functools import partial

import scrapy

from crawlers.items import TendaItem
from crawlers.spiders import BaseSpider

# from scrapy.shell import inspect_response


header = {
    "accept": "*/*",
    "accept-encoding": "*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://www.tendaatacado.com.br",
    "referer": "https://www.tendaatacado.com.br/",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "cookie": "_gac_UA-42869860-3=1.1678478371.Cj0KCQiAx6ugBhCcARIsAGNmMbgxiv-4-fBu9qHSnvWBRvhHrA_CYkJVExt8sEGs8JiU0paX20_JR7kaAkm_EALw_wcB; _gcl_aw=GCL.1678478371.Cj0KCQiAx6ugBhCcARIsAGNmMbgxiv-4-fBu9qHSnvWBRvhHrA_CYkJVExt8sEGs8JiU0paX20_JR7kaAkm_EALw_wcB; _gcl_au=1.1.873011192.1678478371; nav_id=4040325f-96cf-444c-84da-b0f5907a72f9; _fbp=fb.2.1678478371623.1536804538; legacy_p=4040325f-96cf-444c-84da-b0f5907a72f9; chaordic_browserId=4040325f-96cf-444c-84da-b0f5907a72f9; legacy_c=4040325f-96cf-444c-84da-b0f5907a72f9; legacy_s=4040325f-96cf-444c-84da-b0f5907a72f9; _hjSessionUser_1377533=eyJpZCI6IjQwOTkzOTI0LWNhZDItNTY1MS1hM2NkLTM2ZDY2NmRjMmI0MiIsImNyZWF0ZWQiOjE2Nzg0NzgzNzEyMjcsImV4aXN0aW5nIjp0cnVlfQ==; _clck=1hrifov|1|fal|0; _gid=GA1.3.1651488331.1680976231; JSESSIONID=CA81F13A850A81AECC4DE485F7F8641E; _hjIncludedInSessionSample_1377533=0; _hjSession_1377533=eyJpZCI6ImU2NWYyYTI0LWZlNTYtNDRjYy04ZjYwLTBkNDVkMzMxNTFhZiIsImNyZWF0ZWQiOjE2ODA5Nzk4MzI3NTUsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ga_G05J2RCJLS=GS1.1.1680979596.3.1.1680979832.60.0.0; _ga=GA1.1.1363611907.1678478371; _uetsid=db2aa2d0d63511ed9e4e7f14e9e14580; _uetvid=db2ae240d63511ed9adb9b435bff11e3; _clsk=1ln5ajd|1680979833188|2|1|y.clarity.ms/collect; impulsesuite_session=1680979833446-0.03889130290069254",
}


class TendaSpider(BaseSpider):
    name = "tenda"

    custom_settings = {"ITEM_PIPELINES": {"crawlers.pipelines.TendaPipeline": 300}}

    def __init__(self, filial=1):  # vou padronizar que a filial 1 é a de são josé dos campos
        super().__init__("TENDA", filial)

    def start_requests(self):
        # cart id não sei se é obrigatório
        yield scrapy.Request(
            "https://api.tendaatacado.com.br/api/public/store/departments",
            callback=self.parse_categorias,
            headers=header,
        )

    def parse(self, response, departamento, categoria, category_id, link):
        jsonresponse = json.loads(response.text)
        produtos = jsonresponse["products"]
        for produto in produtos:
            if produto["availability"] != "in_stock":
                continue
            # brandToken -> tá bom de colocar a marca dos produtos, ajuda na pesquisa
            codigo_de_barras = produto["barcode"]
            # wholesalePrices [{minQuantity: 12, price: 4.59}] -> é o preço de atacado!
            yield TendaItem(
                item=codigo_de_barras,
                nome=produto["name"],
                categoria=categoria,
                departamento=departamento,
                preco=produto["price"],
            )
        parse_categoria = partial(
            self.parse, departamento=departamento, categoria=categoria, category_id=category_id, link=link
        )
        # se tem mais páginas, então crawleia elas
        if jsonresponse["current_page"] == 1 and jsonresponse["total_pages"] > 1:
            for page in range(2, jsonresponse["total_pages"] + 1):
                url = "https://api.tendaatacado.com.br/api/public/store/category/{category_id}/products?query=%7B%22link%22:%22{link}%22%7D&page={page}&order=relevance&save=true&cartId=6262166"
                yield scrapy.Request(
                    url.format(category_id=category_id, link=link, page=page), callback=parse_categoria, headers=header
                )

    def parse_categorias(self, response):
        # inspect_response(response, self)
        categorias_tree = json.loads(response.text)
        for dep in categorias_tree:
            for cat in dep["children"]:
                parse_categoria = partial(
                    self.parse, departamento=dep["name"], categoria=cat["name"], category_id=cat["id"], link=cat["link"]
                )
                url = "https://api.tendaatacado.com.br/api/public/store/category/{category_id}/products?query=%7B%22link%22:%22{link}%22%7D&page={page}&order=relevance&save=true&cartId=6262166"
                yield scrapy.Request(
                    url.format(category_id=cat["id"], link=cat["link"], page=1),
                    callback=parse_categoria,
                    headers=header,
                )
