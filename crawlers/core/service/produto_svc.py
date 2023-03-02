from core.models import Produto, ProdutoCrawl, Crawl
from datetime import datetime, timedelta

# deve ter um jeito de otimizar a busca
# vou usar o django qserializer do Iuri?
def search_produtos(search_term):
    produto_qs = Produto.objects.filter(search_term=search_term) # produtos que dão match
    crawl_qs = Crawl.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=7)
    ).order_by("-created_at").distinct("mercado") # crawl mais recente de cada mercado
    produto_crawl_qs = ProdutoCrawl.objects.filter(produto__in=produto_qs, crawl__in=crawl_qs).select_related("crawl", "crawl__mercado", "produto")  # pegar só o Crawl mais recente de cada mercado
    return produto_crawl_qs
    # o que o front deseja saber é isso aqui agrupado por produto ou por mercado? ( talvez até pelos 2 )