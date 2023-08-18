import time
import os
import pickle
import json
import sys
import base64
import requests


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


def pdf_converter(driver, selector):
    pdf_button = driver.find_element(selector.XPATH, "/html/body/div/div[2]/div[4]/button")
    pdf_button.click()
    pdf_link = driver.current_url
    
    response = requests.get(pdf_link)
    pdf_content = response.content
    pdf_base64 = base64.b64encode(pdf_content).decode("utf-8")

    return pdf_base64


def dict_to_json(dict):
    json_data = json.dumps(dict, ensure_ascii=False, indent=4)
    output_file = "dados_consulta.json"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(json_data)

    print("JSON salvo com sucesso em:", output_file)
    print(json_data)


def table_to_dict(data):
    table_rows = data.split('\n')
    table_data = []
    for row in table_rows[1:]:
        columns = row.split(' ')
        data = {
        "Data Inicial": columns[0],
        "Data Final": columns[1],
        "Detalhamento": ' '.join(columns[2:])
        }
        table_data.append(data)
    return table_data


def consultar_simples_nacional_scrap(cnpj):
    delay = 10
    url = "https://consopt.www8.receita.fazenda.gov.br/consultaoptantes"
    opcoes = uc.ChromeOptions()
    opcoes.add_argument("--headless")
    browser = uc.Chrome(options=opcoes)

    browser.get(url)

    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
    time.sleep(2)

    cnpj_input = browser.find_element(By.NAME, "Cnpj")
    time.sleep(1)

    if os.path.isfile("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))

    for cookie in cookies:
        browser.add_cookie(cookie)
    time.sleep(1)

    cnpj_input.send_keys(cnpj)
    time.sleep(2)

    input_text = WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-control"))
    )

    input_text = WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-control"))
    )
    input_text.send_keys(cnpj)

    button_text = browser.find_element(by=By.CLASS_NAME, value="btn-verde")
    time.sleep(1)
    button_text.click()

    WebDriverWait(browser, delay * 4).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "spanValorVerde"))
    )


    more_info_button = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[3]/div[1]/button")
    more_info_button.click()

    time.sleep(2)
    consult_data = browser.find_element(By.XPATH, "/html/body/div/div[2]/h5/span").text
    bussines_name = browser.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/span[3]').text
    sn_status = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/span[1]").text
    options_table = browser.find_element(By.XPATH, "/html/body/div/div[2]/div[3]/div[2]/div[1]/div[2]/table").text
    table = table_to_dict(options_table)

    pdf_64 = pdf_converter(browser, By)

    browser.quit()

    data_dict = {
    "Data da consulta": consult_data,
    "Nome empresarial": bussines_name,
    "Situação no Simples Nacional": sn_status,
    "Períodos anteriores": table,
    "PDF em base64": pdf_64
    }

    dict_to_json(data_dict)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <cnpj>")
        sys.exit(1)

    cnpj = sys.argv[1]
    consultar_simples_nacional_scrap(cnpj)
