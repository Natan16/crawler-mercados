from core.service import produto_svc
from django.http import JsonResponse
from django.shortcuts import render


def search_produtos(request):
    search_term = request.GET.get("search_term")
    produto_crawl_qs = produto_svc.search_produtos(search_term)

    return render(request, "produtos.xml", {"resposta": [prod.to_dict_json() for prod in produto_crawl_qs]})
    # return JsonResponse()
    # serialized_produto_crawl = [
    #     {
    #         "produto": produto_crawl.produto.to_dict_json(),
    #         "mercado": produto_crawl.crawl.mercado.to_dict_json(),
    #         "preco": produto_crawl.preco,
    #     }
    #     for produto_crawl in produto_crawl_qs
    # ]
    # return JsonResponse(serialized_produto_crawl, safe=False)

