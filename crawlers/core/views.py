import json

from django.http import JsonResponse

from core.forms import MercadosProximosForm
from core.service.mercado_svc import mercados_proximos
from core.service.produto_svc import produtos_mercados_proximos


def search_produtos(request):
    search_term = request.GET.get("search_term")
    mercados_proximos = json.loads(request.GET.get("mercados_proximos", "[]"))
    limit = 50
    response = produtos_mercados_proximos(search_term, mercados_proximos, limit)
    return JsonResponse(response, safe=False)


def get_mercados_proximos(request):
    form = MercadosProximosForm.parse_raw(request.GET.get("params"))
    mercados_e_distancias = mercados_proximos(form.latitude, form.longitude, form.raio, form.redes)
    response = []
    for mercado, _ in mercados_e_distancias:
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
