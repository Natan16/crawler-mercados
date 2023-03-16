import operator
from core.models import Produto, ProdutoCrawl, Crawl
from datetime import datetime, timedelta
from django.db.models import CharField, Q
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
    ).order_by('created_at')
    mercado_crawl_map = {}
    for crawl in crawl_qs:
        mercado_crawl_map[crawl.mercado.pk] = crawl
    # tem que agrupar junto produtos iguais, e deixar próximo produtos parecidos só depois ordena por preço. Como fazer isso?
    # a search boa é a chave pra um bom produto
    # o peso igual é que é interessante ter ... não que não possa ser pesquisado
    produto_crawl_qs = ProdutoCrawl.objects.filter(produto__in=produto_qs, crawl__in=mercado_crawl_map.values()).select_related("crawl", "crawl__mercado", "produto").order_by("preco")
    # tem que priorizar correspondências exatas, só depois olha pro preço. Priorizar quando começa com o texto também
    # se tem que começa com o texto ( exato ) ... não é bom por causa de Coca cola e Refrigerante Coca cola
    return produto_crawl_qs
