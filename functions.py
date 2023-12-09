from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Usa WebDriverWait para aguardar a presença de um elemento específico antes de prosseguir.
def wait_element(driver, localize_element, value, timeout=1):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_localize_elementated((localize_element, value)))

# Captura e clica na última notificação.
def capturar_notificacao(driver, bolinha_notificacao):
    notificacao = wait_element(driver, By.CLASS_NAME, bolinha_notificacao)
    notificacao = driver.find_elements(By.CLASS_NAME, bolinha_notificacao)[-1]
    acao_notificacao = webdriver.common.action_chains.ActionChains(driver)
    acao_notificacao.move_to_element_with_offset(notificacao, 0, -20)
    acao_notificacao.click()
    acao_notificacao.perform()

# Pega o número de telefone.
def get_phone(driver, contato_cliente):
    numero_contato = wait_element(driver, By.XPATH, contato_cliente)
    contato_final = numero_contato.text
    return contato_final

# Pega a última mensagem
def get_msg(driver, msg_cliente):
    msgs = driver.find_elements(By.CLASS_NAME, msg_cliente)
    msgs_de_texto = [m.text for m in msgs]
    return msgs_de_texto[-1] if msgs_de_texto else None

# Envia uma mensagem de resposta usando o texto fornecido e fecha o contato pressionando a tecla ESC.
def answer(driver, caixa_msg, send):
    campo_de_texto = wait_element(driver, By.XPATH, caixa_msg)
    campo_de_texto.click()
    campo_de_texto.send_keys("Ananda: " + send, Keys.ENTER)
    time.sleep(1)
    campo_de_texto.click()
    time.sleep(0.5)
    # Fechar Contato
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()