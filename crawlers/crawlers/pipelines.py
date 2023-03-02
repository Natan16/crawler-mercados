# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from core.models import Produto

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ShibataPipeline:

    def __init__(self):
        pass

    def process_item(self, shibata_item, spider):
        prod = Produto(
            item=shibata_item["item"],
            nome=shibata_item["nome"],
            categoria=shibata_item["categoria"],
            departamento=shibata_item["departamento"],
            peso_liquido=shibata_item["peso_liquido"],
            peso_bruto=shibata_item["peso_bruto"]
        )
        spider.produtos_map[shibata_item["item"]] = (prod, shibata_item["preco"])
    
    def close_spider(self, spider):
        spider.armazena_no_banco()