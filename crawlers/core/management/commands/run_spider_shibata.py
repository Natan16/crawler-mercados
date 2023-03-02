from django.core.management.base import BaseCommand
from crawlers.spiders.spider_shibata import ShibataSpider
from scrapy.crawler import CrawlerProcess

class Command(BaseCommand):
    def handle(self, *args, **options):
        process = CrawlerProcess()
        process.crawl(ShibataSpider)
        process.start()
        