from config import config_driver
from functions import answer, capturar_notificacao, get_msg, get_phone
import time
import requests

# Captura notificações, obtém informações de contato e mensagem, envia uma solicitação para uma API de chatbot personalizada e responde a mensagens recebidas.
def chatbot(driver, notification, contato_cliente, msg_cliente, caixa_msg, usuario, agent):
    try:
        capturar_notificacao(driver, notification)
        contato_final = get_phone(driver, contato_cliente)
        msg = get_msg(driver, msg_cliente)

        if msg:
            # Envia a mensagem para a API do chatbot e obtém a resposta.
            response = requests.get("http://localhost/bot/index.php?", params={'msg': msg, 'contato': contato_final, 'usuario': usuario}, headers=agent)
            
            # Verifica se a resposta da API foi bem-sucedida
            if response.status_code == 200:
                send = response.text
                answer(driver, caixa_msg, send)
                print(f"Mensagem respondida para {contato_final}: {send}")
            else:
                print(f"Falha na solicitação à API. Código de status: {response.status_code}")

    except Exception as e:
        # Lida com exceções específicas e imprime mensagens de erro.
        print(f"Erro durante o processamento: {e}")

if __name__ == "__main__":
    # Configurações iniciais e obtenção de informações da API.
    agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    api = requests.get("https://editacodigo.com.br/index/api-whatsapp/OdhAX4NIw5XP9zUbEEt6CMKNoVbAoUSU", headers=agent)
    time.sleep(1)
    api = api.text
    api = api.split(".n.")
    notification = api[3].strip()
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
        chatbot(driver, notification, contato_cliente, msg_cliente, caixa_msg, usuario, agent)
