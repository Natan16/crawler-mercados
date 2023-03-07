# crawler-mercados
Crawleia os principais supermercados de são josé dos campos pra saber onde os preços estão mais baixos

# Rodar os crawlers
scrapy crawl shibata
scrapy crawl spani

# Subir a aplicação
docker-compose


# próximos passos
buildar imagem docker e colocar ela no ECR
deployar num pod do kubernetes
comprar um domínio no route 53
configurar o ingress com NGINX
https://nahuelhernandez.com/blog/ingress_and_external_dns_with_route53_on_eks/

kubectl apply -f manifests/.


# Bizu pra criar os mercados
from core.models import Mercado

Mercado.objects.create(
    rede = "SHIBATA",
    cidade = "São José dos Campos",
    uf = "SP",
    bairro = "Jardim Oriente",
    unidade = "Shibata - Jardim Oriente",
    filial = 1
)

Mercado.objects.create(
    rede = "SPANI",
    cidade = "São José dos Campos",
    uf = "SP",
    bairro = "Aquarius",
    unidade = "Spani - Aquarius",
    filial = 1
)