import operator
from core.models import Produto, ProdutoCrawl, Crawl
from datetime import datetime, timedelta
from django.db.models import CharField, Q, Prefetch, Avg
from django.db.models.functions import Lower
from functools import reduce
from numpy import mean
from functools import partial


CharField.register_lookup(Lower)

def _sort_produto(produto, words):
    # a ideia aqui seria um preço médio por quantidade se não especificada uma
    preco_medio = float(mean(list(produto.produtocrawl_set.all().values_list("preco", flat=True))))
    if produto.nome.lower().split()[0] == words[0].lower():
        return -1000 + preco_medio
    return preco_medio 


def search_produtos(search_term):
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

    produto_qs.prefetch_related(
        Prefetch("produtocrawl_set", ProdutoCrawl.objects.filter(crawl__in=mercado_crawl_map.values()).select_related("produto", "crawl__mercado"))
    ).distinct()
    # .annotate(preco_medio=Avg("produtocrawl__preco")).order_by("preco_medio") # preco médio e índice de correspondência
    # já resolver essa queryset pra ordenar em memória? Fica ruim por causa da paginação
    sorted_produtos = sorted(produto_qs, key=partial(_sort_produto, words=words)) 
    return sorted_produtos
    # o que melhora índice de correspondência? 
    # -> matches exatos
    # -> mesma ordem
    # -> quantidade
    # -> mostrar o que tem menos texto prependado
    # palavras chave tipo sabor ... perde ponto. nome da fruta tem que mostrar a fruta antes do resto