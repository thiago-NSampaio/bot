import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configuração do WebDriver para salvar a sessão do navegador.
def config_driver():
    dir_path = os.getcwd()
    chrome_options = Options()
    chrome_options.add_argument(r"user-data-dir=" + dir_path + "/pasta/sessao")
    driver = webdriver.Chrome(chrome_options)
    driver.implicitly_wait(1) 
    return driver