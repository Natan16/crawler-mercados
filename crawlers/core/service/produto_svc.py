from core.models import Produto, ProdutoCrawl, Crawl
from datetime import datetime, timedelta
from django.db.models import CharField
from django.db.models.functions import Lower

CharField.register_lookup(Lower)

# deve ter um jeito de otimizar a busca
# vou usar o django qserializer do Iuri?
# TODO: fazer a paginação
def search_produtos(search_term):
    produto_qs = Produto.objects.filter(nome__search=search_term)
    crawl_qs = Crawl.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=7)
    )
    produto_crawl_qs = ProdutoCrawl.objects.filter(produto__in=produto_qs, crawl__in=crawl_qs).select_related("crawl", "crawl__mercado", "produto").order_by("preco")  # pegar só o Crawl mais recente de cada mercado
    return produto_crawl_qs
