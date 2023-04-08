import operator
from core.models import Produto, ProdutoCrawl, Crawl
from datetime import datetime, timedelta
from django.db.models import CharField, Q, Prefetch
from django.db.models.functions import Lower
from functools import reduce
from numpy import mean
from functools import partial


CharField.register_lookup(Lower)

def _sort_produto(produto, words):
    preco_medio = float(mean(list(produto.produtocrawl_set.all().values_list("preco", flat=True))))
    if produto.nome.strip().lower().split()[0] == words[0].lower():
        return preco_medio - 1000
    # mesma ordem ganha de ordem bagunçada
    # o problema maior é a correspondência entre produtos e não o algoritmo da busca em si
    return preco_medio


def produtos(search_term):
    words = search_term.split()
    # isso aqui vai fazer full table scan
    query = reduce(operator.and_, (Q(nome__lower__unaccent__icontains=word) for word in words))
    produto_qs = Produto.objects.filter(query)
    crawl_qs = Crawl.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=7)
    ).order_by("-created_at")
    mercado_crawl_map = {}
    for crawl in crawl_qs:
        if crawl.mercado.pk in mercado_crawl_map:
           continue
        mercado_crawl_map[crawl.mercado.pk] = crawl

    produto_qs = produto_qs.prefetch_related(
        Prefetch(
            lookup="produtocrawl_set",
            queryset=ProdutoCrawl.objects.filter(
                crawl__in=mercado_crawl_map.values()
            ).select_related("produto", "crawl__mercado").order_by("preco"),
            to_attr="produtocrawl_recente")
    )
    # .annotate(preco_medio=Avg("produtocrawl__preco")).order_by("preco_medio") # preco médio e índice de correspondência
    # já resolver essa queryset pra ordenar em memória? Fica ruim por causa da paginação
    sorted_produtos = sorted(produto_qs, key=partial(_sort_produto, words=words))
    return sorted_produtos
    # ser capaz de identificar e separar tipo de produto e marca ... a separação pode acontecer no próprio banco
    # mostrar esses respostar de segunda classe como resultado à parte e, quem sabe, de maneira mais condensada