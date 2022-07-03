from dataclasses import replace
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from core.models import Mercado, Produto, Crawl, ProdutoCrawl
from decimal import Decimal as D
import re


BASE_URL = 'http://cliqueeretire.shibata.com.br'

def escolher_loja():
    # seleciona cidade
    cidade_select = navegador.find_element(By.XPATH, '//select[@aria-label="Escolha uma cidade"]')
    cidade_select.click()
    cidade_select.send_keys('S')
    cidade_select.send_keys(Keys.ENTER)
    sleep(1)
    # seleciona loja
    loja_select = navegador.find_element(By.XPATH, '//select[@aria-label="Escolha uma loja"]')
    loja_select.click()
    loja_select.send_keys('S')
    loja_select.send_keys(Keys.ENTER)
    sleep(1)
    # clica em escolher
    escolher_button = navegador.find_element(By.XPATH, '//button[@onclick="persistLoja()"]')
    escolher_button.click()

def crawlear_categoria(link):
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

def constroi_dicionario_de_links(departamentos, deps_dict):
    for dep in departamentos:
        navegador.fullscreen_window()
        span = dep.find_element(By.TAG_NAME, 'span')
        div = dep.find_element(By.TAG_NAME, 'div')
        ancoras = div.find_elements(By.TAG_NAME, 'a')
        deps_dict[span.text] = {}
        cats_dict = deps_dict[span.text] 
        for a in ancoras:
            link = a.get_attribute('href')
            cats_dict[a.get_attribute('innerHTML')] = link

# proxybroker serve --host 127.0.0.1 --port 8888 --types HTTP HTTPS --lvl High
# PROXY = 'http://localhost:8888'
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options = ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_experimental_option("prefs", prefs)
navegador = Chrome(options=chrome_options)

navegador.get(BASE_URL)
sleep(2)
escolher_loja()
navegador.fullscreen_window()
sleep(1)
departamentos = navegador.find_elements(By.XPATH, '//div[@data-type="departamentos-nav"]')
deps_dict = {}
constroi_dicionario_de_links(departamentos, deps_dict)
sleep(1)
produtos_a_criar = [] # bulk_create não volta os ids, será que dá certo mesmo assim???
produtos_crawl = []
mercado = Mercado.objects.get(unidade='Shibata - Shopping Jardim Oriente')
crawl = Crawl.objects.create(mercado=mercado)


produtos_map = {}
for dep, cats_dict in deps_dict.items():
    for cat, link in cats_dict.items():
        try:
            produtos = crawlear_categoria(link)
            for str_nome, str_preco in produtos:
                produtos_map[str_nome.lower()] = (str_preco, cat.lower(), dep.lower()) # pode virar dataclass
        except NoSuchElementException: # nesse caso não tem nenhum produto disponível da categoria
            pass

# TODO: parte desse código pode virar parte de um utilitário que vai ser útil pra vários
# crawlers
# esse passo a passo de gravar os dados crawleados é mais ou menos o mesmo
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

Produto.objects.bulk_create(produtos_a_criar, batch_size=1000)
produtos_existentes = Produto.objects.filter(
    item__in=produtos_map.keys()
).in_bulk(field_name='item')

for item, values in produtos_map.items():
    str_preco, _, _ = values
    produtos_crawl.append(ProdutoCrawl(
        preco=str_preco.replace(',', '.')[2:],
        crawl=crawl,
        produto=produtos_existentes[item]
    ))
ProdutoCrawl.objects.bulk_create(produtos_crawl, batch_size=1000)   

navegador.quit()