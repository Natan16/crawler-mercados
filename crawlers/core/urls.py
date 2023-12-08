from django.urls import path

from core import views

urlpatterns = [
    path("api/whoami", views.whoami),
    path("api/search", views.search_produtos),
    path("api/get_mercados_proximos", views.get_mercados_proximos),
]
