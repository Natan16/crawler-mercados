import json
import re
from decimal import Decimal as D
from functools import partial

import scrapy
from core.models import Crawl, Mercado, Produto, ProdutoCrawl
from crawlers.items import CarrefourItem
from scrapy.shell import inspect_response


header = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "cookie": "ambiente=mercado; aconteceu_redirect=true; bm_sz=1B8B55C475A17DAD8261E7CDD15C10FE~YAAQXzEGyXyYOr6GAQAA4Ell0BO0Oc1Mbuutm2iWju5VqkKgYn7BLGKlbkhTFEsjGtXXFs0HceVOwog247GduRTsizzrfzkT2BB9sZRfHFnczfVt9v9hacBx6ToUK72H+GzEafbanLirBi82KRa5UTXw6sXTGRA/KHyZIqKcu/NcoapMyKkAlnDYfwK5Vir2QPljeN5G6VYAqs+eaa6luG9d6ZbJxxYeJE4RtuOcGIWl2rkNPTSecAvn7DGfhbaKyU/Ezpzo9mRNG39qofddTv2hLEgA/mdw675bdMXdH6JYprjQEfm/d+o=~4604994~4273478; ak_bmsc=D1944286EB5CA9259A4D688FAEC7DCDC~000000000000000000000000000000~YAAQXzEGyX+YOr6GAQAA+kpl0BMNT5DnBmsAKtA12LXz7HVClEF5QKBRZXMPSxbqVUKQ7Oqsz98tGeSQ5qFm+NjvstGkGKgqZd+gOYoL06wjFIMVKJe2a/liCZ58N8Cs4AlbMTadzYNl1equsuBb6jdb+fhelDancIwQgayeY3GdfJoP7i8fKdbh0A1aRMdnJTBjy2DQTa1C0KVnK6Dl5B1G+Zcxeys+aljCJ4PlBQvlWuacFBkD1c5gUHs16pt8iHnPJw6IEf+C34NbbAXUf716pLRhoKlHgqtbp3nYmK+KB16rJfkRtiWvscAchElHiiQEX5DVqFTaDPab1JitOBz3sdpB0Fk/uiy2Ya0/+0XYqjGs9CDsMEBdkIJcOqj9NPYqG/OaDyyQbv+2u5tWhg==; _gcl_au=1.1.1735780835.1678533545; _gid=GA1.3.2146779292.1678533546; _vv_source=direct; _vv_deduplication=false; _clck=b05ufm|1|f9t|0; _abck=2C97ADAFF533C87A237E044D5FBD7FD3~0~YAAQXzEGyZKYOr6GAQAAu1Bl0AnVpyWdXMEobM/XWodxte3A9I32BUICGquZVBig+bCC+r17OcArW+dVs0RoC64j9XhTkOqhG+ItfHHgV9g4ZvghWemlrmJ7/aKuq93f6v6t8cQFBHx7MpLKDPJ5i6Z/OLlnVrg6jIUfeKOn6dkpxomD6JkPm5+h/3wZd/SZB0xsy6lzJBo1zJOA3StTg7H3BCbO+/LgOdVvRnRhetc4qgaGGPejc0O7q7i/ef/8FPCjCLRiiIxee+svLWP7+C7BssNQbDWcuBQF4aMJCKN6x8mVrMtP7rX948jp49wfpjlmmAI8yfchYyNjh8EkxZzCoaajz188VrHieUIpQ8t3ACygg7NqWyOzlUzQKEwPdhNLDMFu5O417tYOqHncXbMhW3th/yG2gneH16w=~-1~||-1||~-1; _fbp=fb.2.1678533546223.549220291; _vv_business_id=7cfd3181-2501-162f-866f-6e05298f12af; _vv_helper=https://collect.vendavalida.com.br/helpers/vtex-food.js; _vv_guid=790e0e2c-8cb3-f71b-e5f0-cd0bff07a1a0; _clsk=3fk8s5|1678533546825|1|1|w.clarity.ms/collect; _vv_wp_status_20210619=optinclicked; _uetsid=89002b20bffe11ed9fed0f105c387204; _uetvid=89007050bffe11eda76bd556caff4857; _gat_UA-130952675-8=1; bm_sv=8AF89FD4583F2C68EFAF4F2FD014C5C0~YAAQXzEGyRGeOr6GAQAAmYxm0BPIrRHJTRBCpjV9VdQbNRZhjrGctHSRBpjgy5LhEAGKQ7noAzqa3mIDGwJtaRH09Y3fEQ2WRyZu20uTMCL1tHFY6kFweXXzH6wxynZmmy52u2nq6YHhMYQGfSCDjTEAB/SNpaSZddjvbAwpteuK8suraGDA8ZV33se00sF3Q4jon/ZGLvhzGZ8mwc8qWSPgRDqKGEItaGbdv1DtJm1277R1btJv5RlpXtSlAkon8Dnx6WObNA==~1; _ga_KDLXNXEZ1Z=GS1.1.1678533545.1.1.1678533627.58.0.0; _ga=GA1.1.198433542.1678533546",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJ2aXBjb21tZXJjZSIsImF1ZCI6ImFwaS1hZG1pbiIsInN1YiI6IjZiYzQ4NjdlLWRjYTktMTFlOS04NzQyLTAyMGQ3OTM1OWNhMCIsInZpcGNvbW1lcmNlQ2xpZW50ZUlkIjpudWxsLCJpYXQiOjE2Nzc0NDg1MTYsInZlciI6MSwiY2xpZW50IjpudWxsLCJvcGVyYXRvciI6bnVsbCwib3JnIjoiNjcifQ.Tr4bmVMXV8uTxlQuv4GZPp0gZ8Ugy2fqbOtQ-ODgUbsYVTfNgDGWqBSlpOEr6EMrFw-oE1sVdZCgS4B442qHJg",
    "content-type": "application/json",
    "organizationid": 67,
    "referer": "https://mercado.carrefour.com.br/",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}


class CarrefourSpider(scrapy.Spider):
    name = "carrefour"
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawlers.pipelines.CarrefourPipeline': 300
        }
    }

    def __init__(self, filial=1):
        self.filial = filial
        self.mercado = Mercado.objects.get(rede="CARREFOUR", filial=filial)
        self.crawl = Crawl.objects.create(mercado=self.mercado)
        self.produtos_map = {}
    
    def start_requests(self):
        chunk_size = 40
        departamentos = ["mercearia", "drogaria", "bebidas", 
                         "acougue-e-peixaria", "frios-e-laticinios",
                         "padaria-e-matinais", "congelados", "hortifruti",
                         "bebe-e-infantil", "limpeza-e-lavanderia",
                         "higiene-e-perfumaria", "utilidades-domesticas",
                         "pet-care"]
        for departamento in departamentos:
            url = "https://mercado.carrefour.com.br/api/graphql?operationName=ProductsQuery&variables=%7B%22first%22%3A{first}%2C%22after%22%3A%220%22%2C%22sort%22%3A%22score_desc%22%2C%22term%22%3A%22%22%2C%22selectedFacets%22%3A%5B%7B%22key%22%3A%22c%22%2C%22value%22%3A%22{departamento}%22%7D%2C%7B%22key%22%3A%22region-id%22%2C%22value%22%3A%22v2.6239EBF4FEF59E866802C479EC638A19%22%7D%2C%7B%22key%22%3A%22channel%22%2C%22value%22%3A%22%7B%5C%22salesChannel%5C%22%3A%5C%222%5C%22%2C%5C%22regionId%5C%22%3A%5C%22v2.6239EBF4FEF59E866802C479EC638A19%5C%22%7D%22%7D%2C%7B%22key%22%3A%22locale%22%2C%22value%22%3A%22pt-BR%22%7D%5D%7D"
            parse_first_dep = partial(self.parse_first, departamento=departamento)
            yield scrapy.Request(url.format(first=chunk_size, departamento=departamento), callback=parse_first_dep, headers=header)

    def parse(self, response, departamento=...):
        parsed_response = json.loads(response.text)["data"]["search"]["products"]
        edges = parsed_response["edges"]
        for edge in edges:
            node = edge["node"]
            preco = node["offers"]["lowPrice"]

            yield CarrefourItem(
                item = f"carrefour-{node['id']}",
                nome = node["name"],
                categoria = None,
                departamento = departamento,
                unidades = node["unitMultiplier"],
                preco = preco
            )
        
    def parse_first(self, response, departamento):
        parsed_response = json.loads(response.text)["data"]["search"]["products"]
        total_count = parsed_response["pageInfo"]["totalCount"]
        url = "https://mercado.carrefour.com.br/api/graphql?operationName=ProductsQuery&variables=%7B%22first%22%3A{first}%2C%22after%22%3A%22{after}%22%2C%22sort%22%3A%22score_desc%22%2C%22term%22%3A%22%22%2C%22selectedFacets%22%3A%5B%7B%22key%22%3A%22c%22%2C%22value%22%3A%22{departamento}%22%7D%2C%7B%22key%22%3A%22region-id%22%2C%22value%22%3A%22v2.6239EBF4FEF59E866802C479EC638A19%22%7D%2C%7B%22key%22%3A%22channel%22%2C%22value%22%3A%22%7B%5C%22salesChannel%5C%22%3A%5C%222%5C%22%2C%5C%22regionId%5C%22%3A%5C%22v2.6239EBF4FEF59E866802C479EC638A19%5C%22%7D%22%7D%2C%7B%22key%22%3A%22locale%22%2C%22value%22%3A%22pt-BR%22%7D%5D%7D"
        chunk_size=100
        for after in range(0, total_count, chunk_size):
            parse_dep = partial(self.parse, departamento=departamento)
            yield scrapy.Request(url.format(first=chunk_size, after=after, departamento=departamento), callback=parse_dep, headers=header)
        
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
                
                match = re.search(r"[0-9]+,{0,1}[0-9]*[g|kg|l|ml]", item)
                if match:
                    quant = match.group().replace(',', '.')
                    if quant[-2:] == 'ml':
                        produto.volume_ml = quant[:-2]
                    elif quant[-2:] == 'kg':
                        produto.peso_liquido = 1000 * D(quant[:-2])
                        produto.peso_bruto = 1000 * D(quant[:-2]) 
                    elif quant[-1:] == 'l':
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
        
            produtos_crawl.append(ProdutoCrawl(
                preco=D(str_preco),
                crawl=self.crawl,
                produto=produtos_existentes[codigo_de_barras]
            ))
        ProdutoCrawl.objects.bulk_create(produtos_crawl, batch_size=1000)   
