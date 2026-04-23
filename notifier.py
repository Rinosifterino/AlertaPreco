"""
Módulo responsável exclusivamente pelo disparo genérico de e-mails via SMTP.
"""

import os
import smtplib
from email.message import EmailMessage

# Constantes globais do servidor SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


def send_email_notification(target_email: str, subject: str, body: str) -> None:
    """
    Envia um e-mail genérico utilizando as credenciais do ambiente (.env).

    As credenciais são extraídas dinamicamente durante a execução da função.

    :param target_email: Endereço de e-mail do destinatário.
    :param subject: Título (assunto) do e-mail.
    :param body: Conteúdo principal da mensagem.
    """
    sender_email = os.getenv("email")
    app_password = os.getenv("app_password")

    if not sender_email or not app_password:
        print("[ERROR] Missing email credentials in the environment.")
        return

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = target_email
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(message)

        print(f"[LOG] Email successfully sent to {target_email}")

    except smtplib.SMTPException as smtp_error:
        print(f"[ERROR] SMTP protocol failure: {smtp_error}")
    except Exception as error:
        print(f"[ERROR] Unexpected failure sending email: {error}")