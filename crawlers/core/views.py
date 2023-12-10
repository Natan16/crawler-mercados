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
    response = {
        [
            "mercado": {"unidade": "Shibata - Jardim Oriente", "rede": "SHIBATA"},
            "produto_crawl": [
                {
                    "id": "12",
                    "preco": "14.69",
                    "nome": "Ketchup Heinz Picante - 397g", # vai vir com quantidade (peso/volume) e unidades ... talvez possa sepearar
                    "produto_id": "345" # o produto id é o suficiente pra fazer a correspondência
                    "tags": ["acima da média"] # essa média vai ser uma média temporal ou relativa aos outros
                    # mercados? A segunda coisa me parece mais interessante, dado que, por causa da inflação no br,
                    # tudo tende a ficar mais caro. Nos casos de escessão é possível pensar numa tag promoção
                    # ou ainda tantos % off pra os casos em que o próprio mercado fornecer isso mostrando
                    # precinho riscado e coisas e tal. Posteriormente dá pra pensar num esquema de computar isso
                    # usando o próprio histórico, que daí é um cadim mais complicado, mas dá pra generalizar
                    # pra todos os mercados ... a propósito, essas tags vão ser computadas à priori para os
                    # produtos, não na hora da busca! Nem sempre vai dar, como por exemplo a tag do mais em conta
                    # pode ser acima/abaixo da média com relação à mesma cidade! Geralmente as pessoas não vão em
                    # outras cidades fazer compras.
                    #  ... um sistema de tags é muito importante pra uma boa tomada de decisão
                    # comparar produtos é mais importante do que comparar listas!
                    # infelizmente nem sempre tem tudo que eu quero e não vou saber isso à priori
                    # é isso daí que lasca ... seria interessante se a visulalizaçaõ da lista tivesse
                    # uma lista compreenssíva de tudo que vai ser comprado que desse uma opção fácil de trocar
                    # de mercado ... me parece o melhor dos mundos

                    # item está barato ou caro => daí pode ter tags de acima da média e abaixo da média
                    # com relação aos outros supermercados considerados ... essa é a resposta
                    # pode ser simplesmente o símbolo com a hint quando fizer um hover encima dele
                    # talvez mais do que o produto id e o nome possa vir coisas utilitárias, como range de preço
                },
                # Ketchup Heinz - 1,033kg R$17.79
                {
                    "id": "67",
                    "preco": "30.90",
                    "nome": "Ketchup Heinz Sachê 7g 192 Unidades", # vai vir com quantidade (peso/volume) e unidades ... talvez possa sepearar
                    "produto_id": "890"
                    "tags": ["mais em conta", "abaixo da média"]
                },
            ],
            # para kits/packs essa lógica do mais em conta não pode ser aplicada, preciso de uma maneira
            # de identificá-los
        ]  # pode vir detalhes dos produtos pra acesso por id, pra não ficar duplicando informação
        # será que isso é necessário mesmo? ... tem que pensar
    }

    # for prod in produto_qs[:limit]:
    #     serialized_produto = {
    #         "id": prod.pk,
    #         "nome": prod.nome,
    #         "produto_crawl": [
    #             {
    #                 "id": pc.pk,
    #                 "mercado": {"unidade": pc.crawl.mercado.unidade, "rede": pc.crawl.mercado.rede},
    #                 "preco": pc.preco,
    #                 "produto_id": prod.pk,
    #                 "produto_nome": prod.nome,
    #             }
    #             for pc in prod.produtocrawl_recente
    #         ],
    #     }
    #     if len(serialized_produto["produto_crawl"]) == 0:
    #         continue
    #     # TODO: construir um serializer decente
    #     response.append(serialized_produto)
    return JsonResponse(response, safe=False)


def get_mercados_proximos(request):
    form = MercadosProximosForm.parse_raw(request.GET.get("params"))
    mercados_e_distancias = mercados_proximos(form.latitude, form.longitude, form.raio, form.redes)
    response = []
    for mercado, distancia in mercados_e_distancias:
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
