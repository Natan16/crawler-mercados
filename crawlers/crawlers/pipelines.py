# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from core.models import Produto


class VipCommercePipeline:
    def __init__(self):
        pass

    def process_item(self, carrefour_item, spider):
        prod = Produto(
            item=carrefour_item["item"],
            nome=carrefour_item["nome"],
            categoria=carrefour_item["categoria"],
            departamento=carrefour_item["departamento"],
            peso_liquido=carrefour_item["peso_liquido"],
            peso_bruto=carrefour_item["peso_bruto"],
        )
        spider.produtos_map[carrefour_item["item"]] = (prod, carrefour_item["preco"])

    def close_spider(self, spider):
        spider.armazena_no_banco()


class CarrefourPipeline:
    def __init__(self):
        pass

    def process_item(self, carrefour_item, spider):
        prod = Produto(
            item=carrefour_item["item"],
            nome=carrefour_item["nome"],
            categoria=carrefour_item["categoria"],
            departamento=carrefour_item["departamento"],
        )
        spider.produtos_map[carrefour_item["item"]] = (prod, carrefour_item["preco"])

    def close_spider(self, spider):
        spider.armazena_no_banco()


class PaoDeAcucarPipeline:
    def __init__(self):
        pass

    def process_item(self, pao_de_acucar_item, spider):
        prod = Produto(
            item=pao_de_acucar_item["item"],
            nome=pao_de_acucar_item["nome"],
            categoria=pao_de_acucar_item["categoria"],
            departamento=pao_de_acucar_item["departamento"],
        )
        spider.produtos_map[pao_de_acucar_item["item"]] = (prod, pao_de_acucar_item["preco"])

    def close_spider(self, spider):
        spider.armazena_no_banco()


class TendaPipeline:
    def __init__(self):
        pass

    def process_item(self, tenda_item, spider):
        prod = Produto(
            item=tenda_item["item"],
            nome=tenda_item["nome"],
            categoria=tenda_item["categoria"],
            departamento=tenda_item["departamento"],
        )
        spider.produtos_map[tenda_item["item"]] = (prod, tenda_item["preco"])

    def close_spider(self, spider):
        spider.armazena_no_banco()
