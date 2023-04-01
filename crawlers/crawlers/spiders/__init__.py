# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from core.models import Crawl, Mercado, Produto, ProdutoCrawl


class BaseSpider(scrapy.Spider):

    def __init__(self, rede, filial):
        self.filial = filial
        self.mercado = Mercado.objects.get(rede=rede, filial=filial)
        self.crawl = Crawl.objects.create(mercado=self.mercado)
        self.produtos_map = {}

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
