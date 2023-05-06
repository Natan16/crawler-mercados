import json
from decimal import Decimal as D
from functools import partial

import scrapy
from scrapy.shell import inspect_response
from crawlers.spiders import BaseSpider

from crawlers.items import VipCommerceItem

header = {
    "Accept": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJ2aXBjb21tZXJjZSIsImF1ZCI6ImFwaS1hZG1pbiIsInN1YiI6IjZiYzQ4NjdlLWRjYTktMTFlOS04NzQyLTAyMGQ3OTM1OWNhMCIsInZpcGNvbW1lcmNlQ2xpZW50ZUlkIjpudWxsLCJpYXQiOjE2Nzc0NDgwNjcsInZlciI6MSwiY2xpZW50IjpudWxsLCJvcGVyYXRvciI6bnVsbCwib3JnIjoiMTYxIn0.RANSjc1q_mpotLABDE1Yr9oEETGEvv_jc-9xdos2JoMAJFTu7VMIBNkM_Sv8q7XblMpCfprDHFsUIR223ZnF0Q",
    "Content-Type": "application/json",
    "OrganizationID": 161,
    "Referer": "https://www.loja.shibata.com.br/",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}


class ShibataSpider(BaseSpider):
    name = "shibata"

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.VipCommercePipeline': 300
        }
    }

    def __init__(self, filial=1, centro_distribuicao=13):
        # não tem como pegar o centro de distribuição de algum canto?
        self.centro_distribuicao = centro_distribuicao
        super().__init__("SHIBATA", filial)

    
    def start_requests(self):
        centro_distribuicao = self.centro_distribuicao
        filial = self.filial
        url = "https://api.loja.shibata.com.br/v1/loja/classificacoes_mercadologicas/departamentos/arvore/filial/{filial}/centro_distribuicao/{centro_distribuicao}"
        yield scrapy.Request(url.format(filial=filial, centro_distribuicao=centro_distribuicao), callback=self.parse_categorias, headers=header)


    def parse(self, response, departamento, categoria):
        jsonresponse = json.loads(response.text)["data"]
        for produto in jsonresponse:
            codigo_de_barras = produto["codigo_barras"]
            yield VipCommerceItem(
                item=codigo_de_barras,
                nome=produto["descricao"],
                categoria=categoria,
                departamento=departamento,
                peso_bruto=None,
                peso_liquido=None,
                unidades = produto["quantidade_unidade_diferente"],
                preco = produto["preco"]
            )

    def parse_categorias(self, response):
        categorias_tree = json.loads(response.text)["data"]
        for dep in categorias_tree:
            for cat in dep["children"]:
                parse_categoria = partial(self.parse, departamento=dep["descricao"], categoria=cat["descricao"])
                secao = cat["classificacao_mercadologica_id"]
                url = "https://api.loja.shibata.com.br/v1/loja/classificacoes_mercadologicas/secoes/{secao}/produtos/filial/{filial}/centro_distribuicao/{centro_distribuicao}/ativos?orderby=produto.descricao:asc"
                yield scrapy.Request(url.format(secao=secao, filial=self.filial, centro_distribuicao=self.centro_distribuicao), callback=parse_categoria, headers=header)
