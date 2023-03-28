import json
import re
from decimal import Decimal as D
from functools import partial

import scrapy
from core.models import Crawl, Mercado, Produto, ProdutoCrawl
from scrapy.shell import inspect_response

from crawlers.items import ShibataItem

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


class ShibataSpider(scrapy.Spider):
    name = "shibata"

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.ShibataPipeline': 300
        }
    }

    def __init__(self, filial=1, centro_distribuicao=14):
        self.centro_distribuicao = centro_distribuicao
        self.filial = filial
        self.mercado = Mercado.objects.get(rede=ShibataSpider.name.upper(), filial=filial)
        self.crawl = Crawl.objects.create(mercado=self.mercado)
        self.produtos_map = {}
        # o spani é na mesma vibe
        # posso até fazer um comando pra criar mercados ... seria legal fazer naquele esquema de template
    
    def start_requests(self):
        centro_distribuicao = self.centro_distribuicao
        filial = self.filial
        url = "https://api.loja.shibata.com.br/v1/loja/classificacoes_mercadologicas/departamentos/arvore/filial/{filial}/centro_distribuicao/{centro_distribuicao}"
        yield scrapy.Request(url.format(filial=filial, centro_distribuicao=centro_distribuicao), callback=self.parse_categorias, headers=header)


    def parse(self, response, departamento, categoria):
        jsonresponse = json.loads(response.text)["data"]
        for produto in jsonresponse:
            codigo_de_barras = produto["produto"]["complemento"]["codigo_barras"]
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
                url = "https://api.loja.shibata.com.br/v1/loja/classificacoes_mercadologicas/secoes/{secao}/produtos/filial/{filial}/centro_distribuicao/{centro_distribuicao}/ativos?orderby=produto.descricao:asc"
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
