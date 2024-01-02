from django.core.management.base import BaseCommand

from core.models import ProdutoCrawl


class Command(BaseCommand):
    def handle(self, *args, **options):
        produto_crawl_qs = ProdutoCrawl.objects.order_by("-id")[:1]
        unique = set()
        produtos_crawl_para_deletar = []
        for produto_crawl in produto_crawl_qs:
            key = produto_crawl.produto.pk
            if key in unique:
                produtos_crawl_para_deletar.append(produto_crawl.pk)
                continue
            unique.add(key)

        ProdutoCrawl.objects.filter(id__in=produtos_crawl_para_deletar).delete()
