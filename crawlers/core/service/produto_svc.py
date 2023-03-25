import operator
from core.models import Produto, ProdutoCrawl, Crawl
from datetime import datetime, timedelta
from django.db.models import CharField, Q, Prefetch
from django.db.models.functions import Lower
from functools import reduce

CharField.register_lookup(Lower)


def search_produtos(search_term):
    words = search_term.split()
    # isso aqui vai fazer full table scan
    query = reduce(operator.and_, (Q(nome__lower__unaccent__icontains=word) for word in words))
    produto_qs = Produto.objects.filter(query)
    crawl_qs = Crawl.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=7)
    ).distinct('mercado').order_by('-created_at', 'mercado')
    produto_qs.prefetch_related(
        Prefetch("produto_crawl_set", ProdutoCrawl.objects.filter(crawl__in=crawl_qs))
    ).annotate() # preco médio e índice de correspondência
    # boa, agora sim, posso computar coisas como preço médio
    # produto_crawl_qs = ProdutoCrawl.objects.filter(produto__in=produto_qs, crawl__in=mercado_crawl_map.values()).select_related("crawl", "crawl__mercado", "produto").order_by("preco")
    # return produto_crawl_qs
