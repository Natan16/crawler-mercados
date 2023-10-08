# crawler-mercados
Crawleia os principais supermercados de São José dos Campos pra saber onde os preços estão mais baixos.
Permite montar listas de compras.
https://mercadosimplificado.com/


# Subir a aplicação
é preciso ter o poetry instalado https://python-poetry.org/docs/#installing-with-the-official-installer

### backend 
```
cd crawlers <!-- daqui em diante tudo é feito dentro desse diretório --> 
<!-- para instalar as dependências -->
poetry install
<!-- para ativar o virtualenv -->
poetry shell
<!-- sobe o banco postgres e o nginx  -->
source dev.sh
dkpgnginx
<!-- num outro terminal -->
poetry shell
./manage.py runserver <!-- na primeira execução é necessário rodar as migrações com ./manage.py migrate e rodar o comando de criar mercados -->   
```
### frontend
```
# é preciso de o npm e o nvm instalados
cd frontend
# pra usar o versão certa do node
nvm use 14
# instala as dependências
npm i
 # roda o frontend
 API_MOCK=0 npm run dev
```


# Rodar os crawlers
Antes de rodar os crawlers é preciso primeiro criar os mecados com 
```
 ./manage.py criar_mercados
scrapy crawl <nome_do_crawler> # p.ex: scrapy crawl spani
```

# Deploy
```
### gera imagem docker e sobe no ECR
make all
#### faz ssh na instância do EC2 que tá rodando a aplicação
ssh -i chave-instancia.pem ubuntu@52.67.123.39
### remove a imagem antiga, baixa a mais atual e roda o container
docker rm -f $(docker ps -a -q)
docker image rm 415395292850.dkr.ecr.sa-east-1.amazonaws.com/crawlers
docker image rm crawlers &&
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 415395292850.dkr.ecr.sa-east-1.amazonaws.com &&
docker pull 415395292850.dkr.ecr.sa-east-1.amazonaws.com/crawlers:latest
docker image tag 415395292850.dkr.ecr.sa-east-1.amazonaws.com/crawlers:latest crawlers:latest &&
docker run --name crawlers -d --env-file /home/ubuntu/crawlers.env         -p 3000:3000 -p 8000:8000         -v /home/ubuntu/dkdata/crawlers:/dkdata         crawlers start_web.sh
```
