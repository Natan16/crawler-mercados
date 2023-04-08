# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserModuleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class VipCommerceItem(scrapy.Item):
    item=scrapy.Field()
    nome=scrapy.Field()
    categoria=scrapy.Field()
    departamento=scrapy.Field()
    peso_bruto=scrapy.Field()
    peso_liquido=scrapy.Field()
    unidades=scrapy.Field()
    preco=scrapy.Field()

class CarrefourItem(scrapy.Item):
    item=scrapy.Field()
    nome=scrapy.Field()
    categoria=scrapy.Field()
    departamento=scrapy.Field()
    unidades=scrapy.Field()
    preco=scrapy.Field()

class PaoDeAcucarItem(scrapy.Item):
    item=scrapy.Field()
    nome=scrapy.Field()
    categoria=scrapy.Field()
    departamento=scrapy.Field()
    preco=scrapy.Field()

class TendaItem(scrapy.Item):
    item=scrapy.Field()
    nome=scrapy.Field()
    categoria=scrapy.Field()
    departamento=scrapy.Field()
    preco=scrapy.Field()
    # logo vai ter o preço de atacado aqui
