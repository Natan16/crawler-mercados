# https://api.spanionline.com.br/v1/loja/classificacoes_mercadologicas/secoes/75/produtos/filial/1/centro_distribuicao/10/ativos?orderby=produto.descricao:asc


import json
from decimal import Decimal as D
from functools import partial

import scrapy
from crawlers.items import VipCommerceItem
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


class SpaniSpider(BaseSpider):
    name = "spani"

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.VipCommercePipeline': 300  # estudar melhor esse negócio de pipelines, pode
            # ter uma pipeline por api, nesse caso é vip commerce
        }
    }

    def __init__(self, filial=1, centro_distribuicao=10):
        self.centro_distribuicao = centro_distribuicao
        super().__init__("SPANI", filial)
    
    def start_requests(self):
        centro_distribuicao = self.centro_distribuicao
        filial = self.filial
        
        url = "https://api.spanionline.com.br/v1/loja/classificacoes_mercadologicas/departamentos/arvore/filial/{filial}/centro_distribuicao/{centro_distribuicao}"
        yield scrapy.Request(url.format(filial=filial, centro_distribuicao=centro_distribuicao), callback=self.parse_categorias, headers=header)

    def parse(self, response, departamento, categoria):
        jsonresponse = json.loads(response.text)["data"]
        for produto in jsonresponse:
            codigo_de_barras = produto["produto"]["complemento"]["codigo_barras"]
            # TODO: renomear pra um nome mais genérico
            yield VipCommerceItem(
                item=codigo_de_barras,
                nome=produto["descricao"],
                categoria=categoria,
                departamento=departamento,
                peso_bruto=D(produto["produto"]["peso_bruto"]) or None,
                peso_liquido=D(produto["produto"]["peso_liquido"]) or None,
                unidades = produto["produto"]["quantidade_unidade_diferente"],
                preco = produto["preco"]
            )
        
    def parse_categorias(self, response):
        categorias_tree = json.loads(response.text)["data"]
        for dep in categorias_tree:
            for cat in dep["children"]:
                parse_categoria = partial(self.parse, departamento=dep["descricao"], categoria=cat["descricao"])
                secao = cat["classificacao_mercadologica_id"]
                url = "https://api.spanionline.com.br/v1/loja/classificacoes_mercadologicas/secoes/{secao}/produtos/filial/{filial}/centro_distribuicao/{centro_distribuicao}/ativos?orderby=produto.descricao:asc"
                yield scrapy.Request(url.format(secao=secao, filial=self.filial, centro_distribuicao=self.centro_distribuicao), callback=parse_categoria, headers=header)

