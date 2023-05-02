from core import views
from django.urls import path

urlpatterns = [
    path('api/whoami', views.whoami),
    path('api/search', views.search_produtos),
    path('api/get_mercados_proximos', views.get_mercados_proximos)
]
