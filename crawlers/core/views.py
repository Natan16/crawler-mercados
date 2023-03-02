from django.shortcuts import render

# Create your views here.


def search_produto(request):
    ...
    # tem pegar os produtos que dê match com os parâmetros de busca e 
    # retornar o crawl mais recente de cada um deles pra cada mercado ( definindo um máximo de dias, claro )
    JsonResponse([] ,safe=False)
