import re
from decimal import Decimal as D
from time import sleep

from core.models import Crawl, Mercado, Produto, ProdutoCrawl
from django.core.management.base import BaseCommand
from selenium.webdriver import Chrome, ChromeOptions

# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class CrawlerSpani:
    BASE_URL = "https://www.spanionline.com.br"



    def __init__(self):
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options = ChromeOptions()
        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
        chrome_options.add_experimental_option("prefs", prefs)
        self.navegador = Chrome(options=chrome_options)
        navegador = self.navegador
        navegador.get(self.BASE_URL)
        navegador.fullscreen_window()
        sleep(5)
        navegador.find_element(By.ID, "cep").click()
        navegador.find_element(By.ID, "cep").send_keys("12241-200")
        sleep(2)
        self.escolher_loja()
        # sleep(100)

    def escolher_loja(self, loja_keys='Spani Aquarius'): #, cidade_keys='São José dos Campos'):
        navegador = self.navegador
        # aqui já é o escolher loja
        navegador.find_element(By.CSS_SELECTOR, ".alterar-loja--opcao:nth-child(2) > .btn").click()
        sleep(1)
        lojas = navegador.find_elements(By.XPATH, '//div[@class="card card-default alterar-loja--opcao-retirada ng-star-inserted"]')
        for loja in lojas:
            if loja_keys in loja.find_element(By.TAG_NAME, 'h6').text:
                loja.find_element(By.TAG_NAME, "button").click()
                break

    def coleta_urls(self):
        departamentos = self.navegador.find_element(By.ID, "departamentos").find_elements(By.TAG_NAME, "li")
        deps_dict = {}
        deps = []
        # reversed_deps_dict = {}
        for departamento in departamentos:
            ancora = departamento.find_element(By.TAG_NAME, 'a')
            dep_name = ancora.find_element(By.XPATH, '//div[@class="text-category"]').text.strip().lower()
            dep_link = ancora.get_attribute('href')
            actions = ActionChains(self.navegador)
            actions.move_to_element(departamento).perform()
            element = self.navegador.find_element(By.CSS_SELECTOR, "body")
            actions = ActionChains(self.navegador)
            actions.move_to_element_with_offset(element, 0, 0).perform()
            # o mouse over tá funcionando
            sleep(100)
            # reversed_deps_dict[dep_link] = dep_name
        # self.navegador.find_element(By.TAG_NAME, 'app-produto-departamento').find_elements(By.TAG_NAME=)
        # script = "return window.getComputedStyle(document.querySelector('i.fa'),':before').getPropertyValue('content')"
        # print(self.navegador.execute_script(script).strip())
        # .getPropertyValue('target-text')
        script = "return [...document.querySelectorAll('i.fa')].map(i => Object.values(window.getComputedStyle(i,':before')))"
        # content
        css = self.navegador.execute_script(script)
        print(css)
        sleep(100)
        # departamentos = self.navegador.find_element(By.ID, "departamentos").find_elements(By.TAG_NAME, "li")
        # deps_dict = {}
        # deps = []
        # for departamento in departamentos:
        #     ancora = departamento.find_element(By.TAG_NAME, 'a')
        #     dep_name = ancora.find_element(By.XPATH, '//div[@class="text-category"]').text.strip().lower()
        #     dep_link = ancora.get_attribute('href')
        #     print(dep_name)
        #     print(dep_link)
        #     deps.append((dep_name, dep_link)) 
        # sleep(1)
        # for dep_name, dep_link in deps:
        #     # url = self.BASE_URL + dep_link
        #     self.navegador.get(dep_link)
        #     sleep(3)
        #     cat_dict = {}
        #     deps_dict[dep_name] = cat_dict 
        #     categorias = self.navegador.find_element(By.XPATH, '//div[@class="row vip-categories"]').find_elements(By.TAG_NAME, 'a')
        #     for categoria in categorias:
        #         cat_name = categoria.text
        #         cat_link = categoria.get_attribute('href')
        #         cat_dict[cat_name] = cat_link
        # self.deps_dict = deps_dict

                
        # row vip-categories
        # ac = ActionChains(self.navegador)
        # ac.move_to_element(departamento).perform()
        # i = departamento.find_element(By.TAG_NAME, "i")

            # my_element_id = 'something123' # preciso saber o id desse cara
            # ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
            # your_element = WebDriverWait(self.navegador, 2,ignored_exceptions=ignored_exceptions)\
            #                         .until(expected_conditions.presence_of_element_located((By.ID, my_element_id)))

            # sleep(100)
            # agora eu vou construir o dicionário de categorias
        # self.deps_dict = deps_dict
        # raise NotImplementedError
        #navegador = self.navegador
        
    # pode ter um método só pra criar os mercados

    def crawleia(self):
        raise NotImplementedError
        self.mercado = Mercado.objects.get(unidade='Spani Aquarius')
        self.crawl = Crawl.objects.create(mercado=self.mercado)
        
    def armazena_no_banco(self):
        # isso aqui pode ser o mesmo pra todo mundo, vai ser da classe pai
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
                # TODO: isolar num método
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

    # def _constroi_dicionario_de_links(self, departamentos, deps_dict):
    #     navegador = self.navegador
    #     for dep in departamentos:
    #         navegador.fullscreen_window()
    #         span = dep.find_element(By.TAG_NAME, 'span')
    #         div = dep.find_element(By.TAG_NAME, 'div')
    #         ancoras = div.find_elements(By.TAG_NAME, 'a')
    #         deps_dict[span.text] = {}
    #         cats_dict = deps_dict[span.text] 
    #         for a in ancoras:
    #             link = a.get_attribute('href')
    #             cats_dict[a.get_attribute('innerHTML').strip()] = link

    def _crawlear_categoria(self, link):
        raise NotImplementedError
        # navegador = self.navegador
        # navegador.get(link)
        # sleep(5)
        # products_area = navegador.find_element(By.ID, 'products-area')
        # div_cards_produto = products_area.find_element(By.XPATH, '//div[@class="row px-0 mx-0"]')
        # nomes = div_cards_produto.find_elements(By.XPATH, '//p[@class="card-title"]')
        # precos = div_cards_produto.find_elements(By.XPATH, '//p[@class="card-text text-success"]')
        # produtos = []
        # for nome, preco in zip(nomes, precos):
        #     produtos.append((nome.text, preco.find_element(By.TAG_NAME, 'strong').text))
        # return produtos


# proxybroker serve --host 127.0.0.1 --port 8888 --types HTTP HTTPS --lvl High
# PROXY = 'http://localhost:8888'
class Command(BaseCommand):

    def handle(self, *args, **options):
        cs = CrawlerSpani()
        cs.coleta_urls()
        # cs.crawleia()
        # cs.armazena_no_banco()