from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from datetime import datetime, timedelta
from django.db.models import Value
from numpy import mean

from core.models import Crawl, Produto, ProdutoCrawl
from collections import defaultdict
from decimal import Decimal
from typing import List


# é, falta só isso aqui mesmo e tá pronto
def _get_id_mais_em_conta(itens: List[ProdutoCrawl]): # aqui talvez seja interessante retornar o índice do mais em conta
    # agrupar por tipo de unidades pra descobrir o mais comum
    for item in itens:
        item.produto.peso_liquido
        item.produto.volume_ml
        # o default é nada
    # primeiro vou escrever do jeito burro e depois refatorar
    # se tiver mais de uma vez é pack, não deveria entrar
    item.preco/(item.produto.unidades * item.produto.medida)


def search_produtos(crawl_produto_crawl_list_map, crawl_mercado_map, produto_preco_medio_map):
    dmercados = []
    for crawl_id, produto_crawl_list in crawl_produto_crawl_list_map.items():
            id_mais_em_conta = _get_id_mais_em_conta(produto_crawl_list) # se for -1 não precisa colocar
            mercado = crawl_mercado_map.get(crawl_id)
            if not mercado:
                continue
            dmercado = {}
            dmercado["mercado"] = {"id": mercado.pk, "unidade": mercado.unidade, "rede": mercado.rede}
            produto_crawl_list = sorted(produto_crawl_list, key=)
            dmercado["produto_crawl"] = []
            for pc in produto_crawl_list:
                dprodutocrawl = {
                    "id": pc.id,
                    "preco": pc.preco,
                    "produto": {
                        "id": pc.produto.pk,
                        "nome": pc.produto.nome
                    },
                    "tags": []
                }
                # coloca tags
                if pc.id == id_mais_em_conta:
                    dprodutocrawl["tags"].append("mais em conta")
                preco_medio = produto_preco_medio_map[pc.produto.id]
                if pc.preco > Decimal("1.05") * preco_medio:
                    dprodutocrawl["tags"].append("acima da media")
                elif pc.preco < Decimal("0.95") * preco_medio:
                    dprodutocrawl["tags"].append("abaixo da media")

                dmercado["produto_crawl"].append(dprodutocrawl)
            dmercados.append(dmercado)


def produtos_mercados_proximos(search_term: str, mercados_proximos: List[int], limit: int = 50):
    """
        procura produtos numa lista de mercados próximos, considerando no máximo limit produtos
    """
    
    # crawls de interesse
    crawl_qs = Crawl.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=8)
    ).select_related("mercado").order_by("mercado_id", "-created_at").distinct("mercado_id")
    if mercados_proximos:
        crawl_qs = crawl_qs.filter(mercado_id__in=mercados_proximos)
    else:
        crawl_qs = crawl_qs[:5]

    # produtos de interesse
    vector = SearchVector("nome", "categoria", "departamento")
    query = SearchQuery(search_term.strip())
    produto_qs = Produto.objects.annotate(
        rank=SearchRank(vector, query, normalization=Value(16))
    ).order_by("-rank")[:limit]
    produto_rank_map = {produto.pk: produto.rank for produto in produto_qs}

    crawl_mercado_map = {}
    for crawl in crawl_qs:
        if crawl.pk in crawl_mercado_map:
            continue
        crawl_mercado_map[crawl.pk] = crawl.mercado


    # ordena produto crawl por rank do produto e depois por preço
    produto_crawl_qs = ProdutoCrawl.objects.filter(
        crawl__in=crawl_qs, produto__in=produto_qs
    ).prefetch_related("produto")
    produto_crawl_list = sorted(list(produto_crawl_qs), key = lambda produto_crawl: (
                -produto_rank_map[produto_crawl.produto.pk], produto_crawl.preco
                )
            )

    crawl_produto_crawl_list_map = defaultdict(list)
    for produto_crawl in produto_crawl_list:
        crawl_produto_crawl_list_map[produto_crawl.crawl_id].append(produto_crawl)

    produto_precos_map = defaultdict(list)
    for produto_crawl in produto_crawl_qs:
        produto_precos_map[produto_crawl.produto.pk].append(produto_crawl.preco) 
    produto_preco_medio_map = {produto_id: mean(precos) for produto_id, precos in produto_precos_map.items()} 
    dmercados = search_produtos(crawl_produto_crawl_list_map, crawl_mercado_map, produto_preco_medio_map)
    
    return dmercados
    