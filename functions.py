from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def wait_element(driver, locator_type, value, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((locator_type, value)))

def capturar_notificacao(driver, bolinha_notificacao):
    try:
        notificacao = wait_element(driver, By.CLASS_NAME, bolinha_notificacao)
        acao_notificacao = ActionChains(driver)
        acao_notificacao.move_to_element_with_offset(notificacao, 0, -20).click().perform()
    except Exception as e:
        print(f"Erro ao capturar notificação: {e}")

def get_phone(driver, contato_cliente):
    try:
        numero_contato = wait_element(driver, By.XPATH, contato_cliente)
        contato_final = numero_contato.text
        return contato_final
    except Exception as e:
        print(f"Erro ao obter número de telefone: {e}")
        return None

def get_msg(driver, msg_cliente):
    try:
        msgs = driver.find_elements(By.CLASS_NAME, msg_cliente)
        msgs_de_texto = [m.text for m in msgs]
        return msgs_de_texto[-1] if msgs_de_texto else None
    except Exception as e:
        print(f"Erro ao obter mensagem: {e}")
        return None

def answer(driver, caixa_msg, send):
    try:
        campo_de_texto = wait_element(driver, By.XPATH, caixa_msg)
        campo_de_texto.click()
        campo_de_texto.send_keys(f"Ananda: {send}", Keys.ENTER)
        wait_element(driver, By.XPATH, caixa_msg)  # Aguarda a presença do campo após enviar a mensagem
        campo_de_texto.click()
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()  # Fecha o contato
    except Exception as e:
        print(f"Erro ao responder: {e}")
