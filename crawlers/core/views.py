import json

from django.http import JsonResponse

from core.forms import MercadosProximosForm
from core.service.mercado_svc import mercados_proximos
from core.service.produto_svc import produtos


def search_produtos(request):
    search_term = request.GET.get("search_term")
    mercados_proximos = json.loads(request.GET.get("mercados_proximos", "[]"))
    limit = 50
    produto_qs = produtos(search_term, mercados_proximos)
    #  a ideia é pensar numa nova serialização que traga as informações por mercado (unidade + rede)
    # isso aqui limitando a 50 produtos ... mantenho isso ao a ideia é aumentar? Seria interessante
    # fazer um lazy load, já que só mostra os primeiros resultados na maioria do casos
    # daí a ordem dos mercados importa
    # response = {
    #     [
    #         "mercado": {"unidade": "Shibata - Jardim Oriente", "rede": "SHIBATA"},
    #         "produto_crawl": [
    #             {
    #                 "id": 12,
    #                 "preco": "14.69",
    #                 "produto": {
    #                     "id": 345
    #                     "nome": "Ketchup Heinz Picante - 397g",
    #                 }
    #                 "tags": ["acima da média"]
    #             },
    #             # Ketchup Heinz - 1,033kg R$17.79
    #             # tá fazendo sentido pensar numa api mock
    #             {
    #                 "id": 67,
    #                 "preco": "30.90",
    #                 "nome": "Ketchup Heinz Sachê 7g 192 Unidades",
    #                 "produto": {
    #                     "id": 890
    #                     "nome": "Ketchup Heinz Picante - 397g",
    #                 }
    #                 "tags": ["mais em conta", "abaixo da média"]
    #             },
    #         ],
    #         # para kits/packs essa lógica do mais em conta não pode ser aplicada, preciso de uma maneira
    #         # de identificá-los
    #     ]  # pode vir detalhes dos produtos pra acesso por id, pra não ficar duplicando informação
    #     # será que isso é necessário mesmo? ... tem que pensar
    # }
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
                    "produto_nome": prod.nome,
                }
                for pc in prod.produtocrawl_recente
            ],
        }
        if len(serialized_produto["produto_crawl"]) == 0:
            continue
        # TODO: construir um serializer decente
        response.append(serialized_produto)
    return JsonResponse(response, safe=False)


def get_mercados_proximos(request):
    form = MercadosProximosForm.parse_raw(request.GET.get("params"))
    mercados_e_distancias = mercados_proximos(form.latitude, form.longitude, form.raio, form.redes)
    response = []
    for mercado, _ in mercados_e_distancias:
        # serialized_mercado = mercado.to_dict_json()
        # serialized_mercado.update({"distancia": distancia})
        response.append(mercado.pk)
    return JsonResponse(response, safe=False)


def whoami(request):
    i_am = (
        {
            "user": _user2dict(request.user),
            "authenticated": True,
        }
        if request.user.is_authenticated
        else {"authenticated": False}
    )
    return JsonResponse(i_am)


def _user2dict(user):
    d = {
        "id": user.id,
        "name": user.get_full_name(),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "permissions": {
            "ADMIN": user.is_superuser,
            "STAFF": user.is_staff,
        },
    }
    return d
