# Request Headers
# https://api.loja.shibata.com.br/v1/loja/classificacoes_mercadologicas/secoes/99/produtos/filial/1/centro_distribuicao/1/ativos?orderby=produto.descricao:asc
# Request Headers
# Accept: application/json
# Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJ2aXBjb21tZXJjZSIsImF1ZCI6ImFwaS1hZG1pbiIsInN1YiI6IjZiYzQ4NjdlLWRjYTktMTFlOS04NzQyLTAyMGQ3OTM1OWNhMCIsInZpcGNvbW1lcmNlQ2xpZW50ZUlkIjpudWxsLCJpYXQiOjE2Nzc0NDgwNjcsInZlciI6MSwiY2xpZW50IjpudWxsLCJvcGVyYXRvciI6bnVsbCwib3JnIjoiMTYxIn0.RANSjc1q_mpotLABDE1Yr9oEETGEvv_jc-9xdos2JoMAJFTu7VMIBNkM_Sv8q7XblMpCfprDHFsUIR223ZnF0Q
# Content-Type: application/json
# OrganizationID: 161
# Referer: https://www.loja.shibata.com.br/
# sec-ch-ua: "Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Linux"
# User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36
import scrapy
from datetime import datetime, timedelta
from pytz import timezone
import json


# header = {
#     "authority": "www.loja.shibata.com.br",
#     "cache-control": "max-age=0",
#     "sec-ch-ua": 'Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Linux"',
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
#     "accept": "application/json",
#     "sec-fetch-site": "same-origin",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-user": "?1",
#     "sec-fetch-dest": "document",
#     "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
# }


header = {
    "Accept": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJ2aXBjb21tZXJjZSIsImF1ZCI6ImFwaS1hZG1pbiIsInN1YiI6IjZiYzQ4NjdlLWRjYTktMTFlOS04NzQyLTAyMGQ3OTM1OWNhMCIsInZpcGNvbW1lcmNlQ2xpZW50ZUlkIjpudWxsLCJpYXQiOjE2Nzc0NDgwNjcsInZlciI6MSwiY2xpZW50IjpudWxsLCJvcGVyYXRvciI6bnVsbCwib3JnIjoiMTYxIn0.RANSjc1q_mpotLABDE1Yr9oEETGEvv_jc-9xdos2JoMAJFTu7VMIBNkM_Sv8q7XblMpCfprDHFsUIR223ZnF0Q",
    "Content-Type": "application/json",
    "OrganizationID": 161,
    "Referer": "https://www.loja.shibata.com.br/",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}


class ShibataSpider(scrapy.Spider):
    name = "shibata"

    # def __init__(self):
        # pass
    # criar um mercado ( ou pegar o que já existe) -> talvez precise de uma nova migração

    def start_requests(self):
        secao = 99
        centro_distribuicao = 1
        filial = 1
        # talvez o yml que me diga o centro_distribuição e a filial
        # tem que dar um jeito de buscar seções, ou então ir testando até um número muito grande
        url = "https://api.loja.shibata.com.br/v1/loja/classificacoes_mercadologicas/secoes/{secao}/produtos/filial/{filial}/centro_distribuicao/{centro_distribuicao}/ativos?orderby=produto.descricao:asc"
        #for url in self.start_urls:
        yield scrapy.Request(url.format(secao=secao, filial=filial, centro_distribuicao=centro_distribuicao), callback=self.parse, headers=header)

    def parse(self, response):
        scrapy.shell.inspect_response(response, self)
        jsonresponse = json.loads(response.data)
        for produto in jsonresponse:
            produto["produto"]["peso_liquido"]
            produto["produto"]["peso_bruto"]
            # talvez seja interessante recriar o meu modelo de dados ... não quero ficar muito acoplado à essa API!
            
            # criar um Crawl
        # aqui eu já poderia salvar no banco !!!
