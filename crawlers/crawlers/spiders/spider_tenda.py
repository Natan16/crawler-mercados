# https://api.spanionline.com.br/v1/loja/classificacoes_mercadologicas/secoes/75/produtos/filial/1/centro_distribuicao/10/ativos?orderby=produto.descricao:asc


import json
import re
from decimal import Decimal as D
from functools import partial

import scrapy
from crawlers.items import TendaItem
from crawlers.spiders import BaseSpider


header = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJ2aXBjb21tZXJjZSIsImF1ZCI6ImFwaS1hZG1pbiIsInN1YiI6IjZiYzQ4NjdlLWRjYTktMTFlOS04NzQyLTAyMGQ3OTM1OWNhMCIsInZpcGNvbW1lcmNlQ2xpZW50ZUlkIjpudWxsLCJpYXQiOjE2Nzc0NDg1MTYsInZlciI6MSwiY2xpZW50IjpudWxsLCJvcGVyYXRvciI6bnVsbCwib3JnIjoiNjcifQ.Tr4bmVMXV8uTxlQuv4GZPp0gZ8Ugy2fqbOtQ-ODgUbsYVTfNgDGWqBSlpOEr6EMrFw-oE1sVdZCgS4B442qHJg",
    "content-type": "application/json",
    "organizationid": 67,
    "origin": "https://www.spanionline.com.br",
    "referer": "https://www.spanionline.com.br/",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}


class TendaSpider(BaseSpider):
    name = "tenda"

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.TendaPipeline': 300
        }
    }

    def __init__(self, filial=1):  # vou padronizar que a filial 1 é a de são josé dos campos
        super().__init__("TENDA", filial)
    
    def start_requests(self):
        # cart id não sei se é obrigatório
        yield scrapy.Request("https://api.tendaatacado.com.br/api/public/store/departments", callback=self.parse_categorias, headers=header)

    def parse(self, response, departamento, categoria, category_id, link):
        jsonresponse = json.loads(response.text)["data"]
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
                preco = produto["price"]
            )
        parse_categoria = partial(self.parse, departamento=departamento, categoria=categoria, category_id=category_id, link=link)
        # se tem mais páginas, então crawleia elas
        if jsonresponse["current_page"] == 1 and jsonresponse["total_pages"] > 1:
            for page in range(2, jsonresponse["total_pages"] + 1):
                url = "https://api.tendaatacado.com.br/api/public/store/category/{category_id}/products?query=%7B%22link%22:%22{link}%22%7D&page={page}&order=relevance&save=true&cartId=6262166"
                yield scrapy.Request(url.format(category_id=category_id, link=link, page=page), callback=parse_categoria, headers=header)
        
    def parse_categorias(self, response):
        categorias_tree = json.loads(response.text)["data"]
        for dep in categorias_tree:
            for cat in dep["children"]:
                parse_categoria = partial(self.parse, departamento=dep["name"], categoria=cat["name"], category_id=cat["id"], link=cat["link"])
                url = "https://api.tendaatacado.com.br/api/public/store/category/{category_id}/products?query=%7B%22link%22:%22{link}%22%7D&page={page}&order=relevance&save=true&cartId=6262166"
                yield scrapy.Request(url.format(category_id=cat["id"], link=cat["link"], page=1), callback=parse_categoria, headers=header)

