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

# Pra criar os segredos que a aplicação vai usar pra se conectar ao banco

kubectl create secret generic -n default postgres-creds --from-literal=DB_HOST=<HOST> --from-literal=DB_PASS=<PASS>
