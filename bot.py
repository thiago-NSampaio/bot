from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import config_driver
import time
import requests

# Usa WebDriverWait para aguardar a presença de um elemento específico antes de prosseguir.
def wait_element(driver, by, value, timeout=1):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((by, value)))

# Captura e clica na última notificação.
def capturar_notificacao(driver, bolinha_notificacao):
    notificacao = wait_element(driver, By.CLASS_NAME, bolinha_notificacao)
    notificacao = driver.find_elements(By.CLASS_NAME, bolinha_notificacao)[-1]
    acao_notificacao = webdriver.common.action_chains.ActionChains(driver)
    acao_notificacao.move_to_element_with_offset(notificacao, 0, -20)
    acao_notificacao.click()
    acao_notificacao.perform()

# Pega o número de telefone.
def get_telefone(driver, contato_cliente):
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

# Captura notificações, obtém informações de contato e mensagem, envia uma solicitação para uma API de chatbot personalizada e responde a mensagens recebidas.
def chatbot(driver, bolinha_notificacao, contato_cliente, msg_cliente, caixa_msg, usuario, agent):
    try:
        capturar_notificacao(driver, bolinha_notificacao)
        contato_final = get_telefone(driver, contato_cliente)
        msg = get_msg(driver, msg_cliente)

        if msg:
            # Envia a mensagem para a API do chatbot e obtém a resposta.
            response = requests.get("http://localhost/bot/index.php?", params={'msg': msg, 'contato': contato_final, 'usuario': usuario}, headers=agent)
            send = response.text
            answer(driver, caixa_msg, send)
            print(f"Mensagem respondida para {contato_final}: {send}")

    except Exception as e:
        # Lida com exceções e imprime mensagens de erro.
        print(f"Erro: {e}")

if __name__ == "__main__":
    # Configurações iniciais e obtenção de informações da API.
    agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    api = requests.get("https://editacodigo.com.br/index/api-whatsapp/OdhAX4NIw5XP9zUbEEt6CMKNoVbAoUSU", headers=agent)
    time.sleep(1)
    api = api.text
    api = api.split(".n.")
    bolinha_notificacao = api[3].strip()
    contato_cliente = api[4].strip()
    msg_cliente = api[6].strip()
    caixa_msg = api[5].strip()
    usuario = 'tiago@email.com'

    # Configura o WebDriver e abre o WhatsApp Web.
    driver = config_driver()
    driver.get('https://web.whatsapp.com/')
    time.sleep(10)

    # Loop principal para monitorar e responder continuamente a mensagens.
    while True:
        chatbot(driver, bolinha_notificacao, contato_cliente, msg_cliente, caixa_msg, usuario, agent)
