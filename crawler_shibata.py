from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep

BASE_URL = 'http://cliqueeretire.shibata.com.br'

def escolher_loja():
    # seleciona cidade
    cidade_select = navegador.find_element_by_xpath('//select[@aria-label="Escolha uma cidade"]')
    cidade_select.click()
    cidade_select.send_keys('S')
    cidade_select.send_keys(Keys.ENTER)
    sleep(1)
    # seleciona loja
    loja_select = navegador.find_element_by_xpath('//select[@aria-label="Escolha uma loja"]')
    loja_select.click()
    loja_select.send_keys('S')
    loja_select.send_keys(Keys.ENTER)
    sleep(1)
    # clica em escolher
    escolher_button = navegador.find_element_by_xpath('//button[@onclick="persistLoja()"]')
    escolher_button.click()

def crawlear_categoria(link):
    navegador.get(link)
    sleep(5)
    products_area = navegador.find_element_by_id('products-area')
    div_cards_produto = products_area.find_element_by_xpath('//div[@class="row px-0 mx-0"]')
    nomes = div_cards_produto.find_elements_by_xpath('//p[@class="card-title"]')
    precos = div_cards_produto.find_elements_by_xpath('//p[@class="card-text text-success"]')
    produtos = []
    for nome, preco in zip(nomes, precos):
        produtos.append((nome.text, preco.find_element_by_tag_name('strong').text))
    return produtos

def constroi_dicionario_de_links(departamentos, deps_dict):
    for dep in departamentos:
        navegador.fullscreen_window()
        span = dep.find_element_by_tag_name('span')
        div = dep.find_element_by_tag_name('div')
        ancoras = div.find_elements_by_tag_name('a')
        deps_dict[span.text] = {}
        cats_dict = deps_dict[span.text] 
        for a in ancoras:
            link = a.get_attribute('href')
            cats_dict[str(a)] = link


# proxybroker serve --host 127.0.0.1 --port 8888 --types HTTP HTTPS --lvl High
PROXY = 'http://localhost:8888'
chrome_options = ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
navegador = Chrome(options=chrome_options)

navegador.get(BASE_URL)
escolher_loja()
navegador.fullscreen_window()
sleep(1)
departamentos = navegador.find_elements_by_xpath('//div[@data-type="departamentos-nav"]')
deps_dict = {}
constroi_dicionario_de_links(departamentos, deps_dict)
sleep(1)
for dep, cats_dict in deps_dict.items():
    for cat, link in cats_dict.items():
        try:
            produtos = crawlear_categoria(link)
            print(produtos)
        except NoSuchElementException: # nesse caso não tem nenhum produto disponível da categoria
            pass
navegador.quit()