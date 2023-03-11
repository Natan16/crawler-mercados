import operator
from core.models import Produto, ProdutoCrawl, Crawl
from datetime import datetime, timedelta
from django.db.models import CharField, Q
from django.db.models.functions import Lower
from functools import reduce

CharField.register_lookup(Lower)

# TODO: fazer a paginação
# colocar adsense

def search_produtos(search_term):
    words = search_term.split()
    # isso aqui vai fazer full table scan
    query = reduce(operator.and_, (Q(nome__lower__unaccent__icontains=word) for word in words))
    produto_qs = Produto.objects.filter(query)
    crawl_qs = Crawl.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=7)
    ).distinct('mercado').order_by('mercado', "-id")
    produto_crawl_qs = ProdutoCrawl.objects.filter(produto__in=produto_qs, crawl__in=crawl_qs).select_related("crawl", "crawl__mercado", "produto").order_by("preco")
    return produto_crawl_qs
