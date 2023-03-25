from core.service import produto_svc
from django.http import JsonResponse
from django.shortcuts import render


def search_produtos(request):
    search_term = request.GET.get("search_term")
    produto_qs = produto_svc.search_produtos(search_term)
    limit = 20
    response = []
    for prod in produto_qs[:limit]:
        for prod_crawl in prod.produtocrawl_set.all():
            if float(prod_crawl.preco) < 0.01:
                continue
            response.append(prod_crawl.to_dict_json())
    return JsonResponse(response, safe=False)

def whoami(request):
    i_am = {
        'user': _user2dict(request.user),
        'authenticated': True,
    } if request.user.is_authenticated else {'authenticated': False}
    return JsonResponse(i_am)


def _user2dict(user):
    d = {
        'id': user.id,
        'name': user.get_full_name(),
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'permissions': {
            'ADMIN': user.is_superuser,
            'STAFF': user.is_staff,
        }
    }
    return d
