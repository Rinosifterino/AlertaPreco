import re
import smtplib
from email.message import EmailMessage

# Constantes globais do servidor SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


class EmailNotifier:
    """
    Classe responsável por gerenciar e disparar notificações por e-mail.

    Utiliza o protocolo nativo SMTP sobre SSL para realizar o envio
    silencioso em segundo plano.
    """

    def __init__(self, sender_email, app_password):
        """
        Inicializa a instância do Notificador de Email.

        :param sender_email: Endereço de e-mail do remetente configurado.
        :param app_password: Senha de aplicativo de 16 dígitos do Google.
        """
        self.sender_email = sender_email
        self.app_password = app_password

    def send_price_alert(self, old_value, new_value, target_email):
        """
        Constrói e envia um e-mail alertando a alteração de valores.

        :param old_value: O valor do item antes da alteração identificada.
        :param new_value: O novo valor atualizado capturado na página.
        :param target_email: O endereço do destinatário que receberá o alerta.
        """
        message = EmailMessage()
        message["Subject"] = "O valor de seu Leilão mudou"
        message["From"] = self.sender_email
        message["To"] = target_email

        body = (
            "o valor mudou.\n"
            f"Valor anterior: {old_value}\n"
            f"Novo Valor: {new_value}"
        )
        message.set_content(body)

        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.login(self.sender_email, self.app_password)
                smtp.send_message(message)

            print(f"[LOG] Email successfully sent to {target_email}.")

        except smtplib.SMTPException as smtp_error:
            print(f"[ERROR] SMTP protocol failure: {smtp_error}")
        except Exception as error:
            print(f"[ERROR] Unexpected failure during execution: {error}")


def request_inputs():
    """
    Coleta e valida o nome de usuário e o e-mail via entrada padrão.

    Garante que o usuário tenha ao menos 3 letras e que o e-mail possua
    uma estrutura de regex válida.

    :return: Tupla contendo o nome do usuário (str) e o e-mail destino (str).
    """
    while True:
        username = input("Username (min. 3 letters): ").strip()
        if username.isalpha() and len(username) >= 3:
            print(f"[LOG] User '{username}' registered.")
            break
        print("[ERROR] Only letters and at least 3 characters allowed.")

    while True:
        email = input("Target email: ").strip()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(pattern, email):
            break
        print("[ERROR] Invalid email format.")

    return username, email