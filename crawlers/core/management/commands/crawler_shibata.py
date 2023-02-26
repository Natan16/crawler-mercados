from django.core.management.base import BaseCommand
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from core.models import Mercado, Produto, Crawl, ProdutoCrawl
from decimal import Decimal as D
import re

class CrawlerShibata:
    BASE_URL = 'http://cliqueeretire.shibata.com.br'

    def __init__(self, loja_keys='S', cidade_keys='S'):
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options = ChromeOptions()
        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
        chrome_options.add_experimental_option("prefs", prefs)
        self.navegador = Chrome(executable_path="/home/natanviana/dev/pessoal/crawler-mercados/chromedriver", options=chrome_options)
        navegador = self.navegador
        navegador.get(self.BASE_URL)
        sleep(2)
        self.escolher_loja(loja_keys, cidade_keys)
        # TODO: aqui tenho que armazenar a unidade já ( pra criar o mercado, caso não exista )
        navegador.fullscreen_window()
        sleep(1)

    def escolher_loja(self, loja_keys, cidade_keys):
        navegador = self.navegador
        # seleciona cidade
        cidade_select = navegador.find_element(By.XPATH, '//select[@aria-label="Escolha uma cidade"]')
        cidade_select.click()
        cidade_select.send_keys(loja_keys)
        cidade_select.send_keys(Keys.ENTER)
        sleep(1)
        # seleciona loja
        loja_select = navegador.find_element(By.XPATH, '//select[@aria-label="Escolha uma loja"]')
        loja_select.click()
        loja_select.send_keys(cidade_keys)
        loja_select.send_keys(Keys.ENTER)
        sleep(1)
        # clica em escolher
        escolher_button = navegador.find_element(By.XPATH, '//button[@onclick="persistLoja()"]')
        escolher_button.click()

    def coleta_urls(self):
        navegador = self.navegador
        departamentos = navegador.find_elements(By.XPATH, '//div[@data-type="departamentos-nav"]')
        deps_dict = {}
        self._constroi_dicionario_de_links(departamentos, deps_dict)
        self.deps_dict = deps_dict
        print(f"URLS: {deps_dict}")
        sleep(1)
    
    def crawleia(self):
        self.mercado, _ = Mercado.objects.get_or_create(
            rede = "SHIBATA",
            cidade = "Sao Jose dos Campos",
            uf = "SP",
            bairro = "Jardim Oriente",
            unidade='Shibata - Shopping Jardim Oriente'
        )
        self.crawl = Crawl.objects.create(mercado=self.mercado)
        produtos_map = {}
        for dep, cats_dict in self.deps_dict.items():
            for cat, link in cats_dict.items():
                try:
                    produtos = self._crawlear_categoria(link)
                    for str_nome, str_preco in produtos:
                        produtos_map[str_nome.lower()] = (str_preco, cat.lower(), dep.lower()) # pode virar dataclass
                except NoSuchElementException: # nesse caso não tem nenhum produto disponível da categoria
                    pass
        self.produtos_map = produtos_map
        self.navegador.quit()

    def armazena_no_banco(self):
        produtos_a_criar = []
        produtos_crawl = []
        produtos_map = self.produtos_map
        produtos_existentes = Produto.objects.filter(
            item__in=produtos_map.keys()
        ).in_bulk(field_name='item')
        for item, values in produtos_map.items():
            if item not in produtos_existentes:
                _, cat, dep = values
                parts = item.split('-')
                produto = Produto(
                    item=item,
                    nome=parts[0],
                    categoria=cat,
                    departamento=dep
                )
                match = re.search(r"[0-9]+,{0,1}[0-9]*[g|kg|l|ml]", item)
                if match:
                    quant = match.group().replace(',', '.')
                    if quant[-2:] == 'ml':
                        produto.volume_ml = quant[:-2]
                    elif quant[-2:] == 'kg':
                        produto.peso_g = 1000 * D(quant[:-2]) 
                    elif quant[-1:] == 'l':
                        produto.volume_ml = 1000 * D(quant[:-1])
                    else:
                        produto.peso_g = quant[:-1]
                produtos_a_criar.append(produto)

        produtos_criados = Produto.objects.bulk_create(produtos_a_criar, batch_size=1000)
        for p in produtos_criados:
            produtos_existentes[p.item] = p

        for item, values in produtos_map.items():
            str_preco, _, _ = values
            produtos_crawl.append(ProdutoCrawl(
                preco=str_preco.replace(',', '.')[2:],
                crawl=self.crawl,
                produto=produtos_existentes[item]
            ))
        ProdutoCrawl.objects.bulk_create(produtos_crawl, batch_size=1000)   

    def _constroi_dicionario_de_links(self, departamentos, deps_dict):
        navegador = self.navegador
        for dep in departamentos:
            navegador.fullscreen_window()
            span = dep.find_element(By.TAG_NAME, 'span')
            div = dep.find_element(By.TAG_NAME, 'div')
            ancoras = div.find_elements(By.TAG_NAME, 'a')
            deps_dict[span.text] = {}
            cats_dict = deps_dict[span.text] 
            for a in ancoras:
                link = a.get_attribute('href')
                cats_dict[a.get_attribute('innerHTML').strip()] = link

    def _crawlear_categoria(self, link):
        navegador = self.navegador
        navegador.get(link)
        sleep(5)
        products_area = navegador.find_element(By.ID, 'products-area')
        div_cards_produto = products_area.find_element(By.XPATH, '//div[@class="row px-0 mx-0"]')
        nomes = div_cards_produto.find_elements(By.XPATH, '//p[@class="card-title"]')
        precos = div_cards_produto.find_elements(By.XPATH, '//p[@class="card-text text-success"]')
        produtos = []
        for nome, preco in zip(nomes, precos):
            produtos.append((nome.text, preco.find_element(By.TAG_NAME, 'strong').text))
        return produtos


# proxybroker serve --host 127.0.0.1 --port 8888 --types HTTP HTTPS --lvl High
# PROXY = 'http://localhost:8888'
class Command(BaseCommand):
    # os argumentos do comando pode ser cidade e unidade ( vai ter valores default )

    def handle(self, *args, **options):
        # o interessante dessa abordagem é que dá pra paralelizar
        cs = CrawlerShibata()  # posso passar aqui os argumentos
        cs.coleta_urls()
        cs.crawleia()
        cs.armazena_no_banco()


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
