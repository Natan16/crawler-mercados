# https://api.spanionline.com.br/v1/loja/classificacoes_mercadologicas/secoes/75/produtos/filial/1/centro_distribuicao/10/ativos?orderby=produto.descricao:asc


import json
import re
from decimal import Decimal as D
from functools import partial

import scrapy
from core.models import Crawl, Mercado, Produto, ProdutoCrawl
from crawlers.items import ShibataItem

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


class SpaniSpider(scrapy.Spider):
    name = "spani"

    def __init__(self, filial=1, centro_distribuicao=10):
        self.centro_distribuicao = centro_distribuicao
        self.filial = filial
        self.mercado = Mercado.objects.get(rede=SpaniSpider.name.upper(), filial=filial)
        self.crawl = Crawl.objects.create(mercado=self.mercado)
        self.produtos_map = {}
    
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
            yield ShibataItem(
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
        
    def armazena_no_banco(self):
        produtos_a_criar = []
        produtos_crawl = []
        produtos_map = self.produtos_map
        produtos_existentes = Produto.objects.filter(
            item__in=produtos_map.keys()
        ).in_bulk(field_name='item')
        for item, values in produtos_map.items():
            if item not in produtos_existentes:
                produto, _ = values
                match = re.search(r"[0-9]+,{0,1}[0-9]*[l|ml]", produto.nome)
                if match:
                    quant = match.group().replace(',', '.')
                    if quant[-2:] == 'ml':
                        produto.volume_ml = quant[:-2]
                    elif quant[-1:] == 'l':
                        produto.volume_ml = 1000 * D(quant[:-1])
                produtos_a_criar.append(produto)

        produtos_criados = Produto.objects.bulk_create(produtos_a_criar, batch_size=1000)
        for p in produtos_criados:
            produtos_existentes[p.item] = p

        for codigo_de_barras, values in produtos_map.items():
            _, str_preco = values
        
            produtos_crawl.append(ProdutoCrawl(
                preco=D(str_preco),
                crawl=self.crawl,
                produto=produtos_existentes[codigo_de_barras]
            ))
        ProdutoCrawl.objects.bulk_create(produtos_crawl, batch_size=1000)   
