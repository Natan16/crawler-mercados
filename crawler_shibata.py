from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from time import sleep

BASE_URL = 'http://cliqueeretire.shibata.com.br'

def escolher_loja():
    cidade_select = navegador.find_element_by_xpath('//select[@aria-label="Escolha uma cidade"]')
    cidade_select.click()
    cidade_select.send_keys('S')
    cidade_select.send_keys(Keys.ENTER)
    sleep(1)
    loja_select = navegador.find_element_by_xpath('//select[@aria-label="Escolha uma loja"]')
    loja_select.click()
    loja_select.send_keys('S')
    loja_select.send_keys(Keys.ENTER)
    sleep(1)
    escolher_button = navegador.find_element_by_xpath('//button[@onclick="persistLoja()"]')
    escolher_button.click()

navegador = Chrome(executable_path='./chromedriver')
navegador.get(BASE_URL)
sleep(2)
escolher_loja()
navegador.fullscreen_window()
sleep(1)
# dá pra fazer isso em paralelo, inclusive
# talvez eu não precise nem escolher loja, se acessar o link direto
departamentos = navegador.find_elements_by_xpath('//div[@data-type="departamentos-nav"]')
deps_dict = {}
for dep in departamentos:
    navegador.fullscreen_window()
    span = dep.find_element_by_tag_name('span')
    div = dep.find_element_by_tag_name('div')
    ancoras = div.find_elements_by_tag_name('a')
    deps_dict[span.text] = {}
    cats_dict = deps_dict[span.text] 
    for a in ancoras:
        # categoria = a.text
        link = a.get_attribute('href')
        cats_dict[str(a)] = link

def crawlear_categoria(link):
    navegador.get(link)
    sleep(10)

sleep(1)
for dep, cats_dict in deps_dict.items():
    for cat, link in cats_dict.items():
        crawlear_categoria(link)

# SEGUNDO E TERCEIRO DIVS
# NO SEGUNDO TEM UM p COM O NOME DO ITEM 
# NO TERCEIRO TEM UM p COM UM STRONG COM O PREÇO
# VOU ACHAR TUDO ISSO DENTRO DO SEGUNDO DIV NO DIV QUE TEM ID = products-area
# QUE CONVENIENTEMENTE TEM O DATA COUNT DIZENDO A QTDE DE ITENS
# É ISSO, SÓ ALEGRIA. UMA VEZ DE POSSE DESSES DADOS, POSSO FAZER O QUE QUISER COM ELES. 
# colocar umas menssagens aqui enquanto tiver crawleando que depois vão ser mandadas pro logger
# iterando sobre as âncoras, consigo pegar os preços
# pegar todos os div com datatype = departamentos-nav
# dentro de cada um deles tem outro div que tem âncoras pras urls de cada categoria
# é o href dessas âncoras que eu preciso pegar, vamo lá!