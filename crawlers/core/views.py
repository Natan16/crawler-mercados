from core.service.produto_svc import produtos
from core.service.mercado_svc import mercados_proximos
from core.forms import MercadosProximosForm
from django.http import JsonResponse


def search_produtos(request):
    search_term = request.GET.get("search_term")
    mercados_proximos = request.GET.get("mercados_proximos")
    limit = 50
    produto_qs = produtos(search_term, mercados_proximos)
    response = []
    for prod in produto_qs[:limit]:
        serialized_produto = {
            "id": prod.pk,
            "nome": prod.nome,
            "produto_crawl": [
                {
                "id": pc.pk,
                "mercado": {"unidade": pc.crawl.mercado.unidade, "rede": pc.crawl.mercado.rede},
                "preco": pc.preco,
                "produto_id": prod.pk,
                "produto_nome": prod.nome
                } for pc in prod.produtocrawl_recente
            ]
        }
        if len(serialized_produto["produto_crawl"]) == 0:
            continue
        # TODO: construir um serializer decente
        response.append(
            serialized_produto
        )
    return JsonResponse(response, safe=False)


def get_mercados_proximos(request):
    form = MercadosProximosForm.parse_raw(request.GET.get("params"))
    mercados_e_distancias = mercados_proximos(form.latitude, form.longitude, form.raio_em_km, form.redes)
    response = []
    for mercado, distancia in mercados_e_distancias:
        # serialized_mercado = mercado.to_dict_json()
        # serialized_mercado.update({"distancia": distancia})
        response.append(mercado.pk)
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
