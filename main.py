from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import sys
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


import urllib.request
import zipfile
from pathlib import Path
import pickle


# def captcha_resolver(key, url, driver):
#     from twocaptcha import TwoCaptcha

#     sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

#     api_key = "79871d0d1bb403a00b8f558716f2b239"

#     solver_config = {
#         "apiKey": "79871d0d1bb403a00b8f558716f2b239",
#         "defaultTimeout": 120,
#         "recaptchaTimeout": 600,
#         "pollingInterval": 10,
#     }

#     solver = TwoCaptcha(**solver_config)

#     try:
#         result = solver.hcaptcha(sitekey=key, url=url)
#         code = result["code"]
#         time.sleep(2)
#         recaptcha_response_element = driver.find_element(By.ID, "h-recaptcha-response")
#         driver.execute_script(
#             f'arguments[0].value = "{code}";', recaptcha_response_element
#         )

#     except Exception as e:
#         sys.exit(e)

#     else:
#         sys.exit("result: " + str(result))


def consultar_simples_nacional(cnpj):
    # options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")  # Execução sem interface gráfica
    # options.add_argument(
    #     "--disable-infobars"
    # )  # Desativar barra de informações do marionete
    # options.add_argument("--disable-extensions")  # Desativar extensões do marionete
    # options.add_argument(
    #     "--disable-dev-shm-usage"
    # )  # Desativar uso de memória compartilhada (pode causar problemas no Firefox)

    # browser = webdriver.Firefox(options=options)

    # Acessar o portal do Simples Nacional
    delay = 10
    url = "https://consopt.www8.receita.fazenda.gov.br/consultaoptantes"
    opcoes = uc.ChromeOptions()
    opcoes.add_argument("--headless")
    browser = uc.Chrome(options=opcoes)
    browser.get(url)
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
    time.sleep(2)
    # Preencher o formulário com o número do CNPJ
    cnpj_input = browser.find_element(By.NAME, "Cnpj")
    time.sleep(1)
    if os.path.isfile("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))

    for cookie in cookies:
        browser.add_cookie(cookie)
    time.sleep(3)
    cnpj_input.send_keys(cnpj)

    # driver2 = driver.get('https://consopt.www8.receita.fazenda.gov.br/consultaoptantes')

    time.sleep(3)
    input_text = WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-control"))
    )

    time.sleep(3)
    input_text = WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-control"))
    )
    input_text.send_keys(cnpj)
    button_text = browser.find_element(by=By.CLASS_NAME, value="btn-verde")

    time.sleep(1)
    button_text.click()
    time.sleep(2)
    WebDriverWait(browser, delay * 4).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "spanValorVerde"))
    )
    optante = browser.find_elements(by=By.CLASS_NAME, value="spanValorVerde")

    # Clicar no botão "Consultar"
    # consultar_button = browser.find_element(By.CLASS_NAME, "btn.btn-verde.h-captcha")
    # consultar_button.click()
    # Simular clique com interação humana
    site_key = get_sitekey(browser)
    print("site key", site_key)
    # captcha_resolver(site_key, url, browser)
    # action = ActionChains(browser)
    # action.move_to_element(consultar_button).perform()
    # time.sleep(5)
    # action.click(consultar_button).perform()

    # Aguardar até que o elemento de data de consulta seja visível
    # new_url_template = "https://consopt.www8.receita.fazenda.gov.br/consultaoptantes/Home/ConsultarCnpj?vc={}"
    # new_url = new_url_template.format(cnpj)
    time.sleep(1)
    # WebDriverWait(driver, 10).until(EC.url_to_be(new_url))
    data_consulta_element = browser.find_element(By.TAG_NAME, "div")
    data_consulta = data_consulta_element.text

    # Aguardar o carregamento dos resultados (ajuste o tempo conforme necessário)

    # Extrair os dados da empresa
    # data_consulta = driver.find_element(
    #     By.NAME,
    #     "conteudo",
    # ).text

    # nome_empresarial = driver.find_element(
    #     By.XPATH,
    #     "/html/body/div/div[2]/div[1]/div[2]/span[3]",
    # ).text
    # situacao_atual = driver.find_element(
    #     By.XPATH,
    #     "/html/body/div/div[2]/div[2]/div[2]/span[1]",
    # ).text

    # Imprimir os dados da empresa
    print("Data da consulta:", data_consulta)
    # print("Nome Empresarial:", nome_empresarial)
    # print("Situação Atual:", situacao_atual)

    # Fechar o navegador
    browser.quit()


def get_sitekey(driver):
    return driver.find_element(By.CLASS_NAME, "h-captcha").get_attribute("data-sitekey")


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Uso: python script.py <cnpj>")
    #     sys.exit(1)

    # cnpj = sys.argv[1]
    consultar_simples_nacional("00.201.139/0001-01")
