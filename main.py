import os
import re
import sys
from dotenv import load_dotenv

from monitor import start_monitoring


def request_inputs() -> str:
    """
    Coleta e valida o e-mail destino via entrada padrão.
    """
    while True:
        email = input("Target email: ").strip()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(pattern, email):
            return email
        print("[ERROR] Invalid email format.")


def main():
    """
    Função principal que orquestra a execução do sistema.
    """
    load_dotenv()

    # Verifica credenciais no ambiente
    sender_email = os.getenv("email")
    sender_password = os.getenv("app_password")
    delay_time = os.getenv("delay_time")

    if not sender_email or not sender_password or not delay_time:
        print("[ERROR] Missing .env variables. Check email, app_password, and delay_time.")
        sys.exit(1)

    try:
        delay_time = int(delay_time)
    except ValueError:
        print("[ERROR] delay_time must be a number.")
        sys.exit(1)

    # Coleta entradas do usuário
    target_email = request_inputs()

    # Validação da URL
    while True:
        url = input("Enter product URL: ").strip()
        url_pattern = r"^https?://[\w\-]+(\.[\w\-]+)+[/#?]?.*$"
        if re.match(url_pattern, url):
            break
        print("[ERROR] Invalid URL format. Please include http:// or https://")

    # Coleta de seletor opcional
    selector = input("Enter CSS/XPath selector (optional, press Enter to skip): ").strip()
    if selector == "":
        selector = None

    # Inicia o loop procedural
    start_monitoring(url, target_email, delay_time, selector)


if __name__ == "__main__":
    main()