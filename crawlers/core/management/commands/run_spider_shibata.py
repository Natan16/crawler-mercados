from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess

from crawlers.spiders.spider_shibata import ShibataSpider


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
        # process = CrawlerProcess()
        # process.crawl(ShibataSpider)
        # process.start()
        # -o bookspider_data.csv # salvar num arquivo pode ser uma boa ... não sei se eliminaria a necessidade de uma pipeline
