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


def produtos(search_term, mercados_proximos):
    words = search_term.split()
    # tem que ter um pré-processamento das palavras
    # ... do que vai consistir isso?
    # identificar o que é quantidade e padronizar 1.5l 1,5l 1,5 l e 1.5 l tem que ser tudo equivalente
    # pode até ter uma forma de selecionar a quantidade ... isso aqui é um bom começo
    # isolar unidades e quantidade em campos separados é fundamental pra fazer comparações
    # aproveitar que tá nessa e já fazer marca também

    query = reduce(operator.and_, (Q(nome__lower__unaccent__icontains=word) for word in words))
    produto_qs = Produto.objects.filter(query)
    crawl_qs = Crawl.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=7)
    ).order_by("-created_at")
    mercado_crawl_map = {}
    for crawl in crawl_qs:
        if mercados_proximos and crawl.mercado.pk not in mercados_proximos:
            continue 
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
    sorted_produtos = sorted(produto_qs, key=partial(_sort_produto, words=words))
    return sorted_produtos