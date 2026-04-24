import pytest
from notifier import send_email_notification

def test_send_email_notification_success(mocker):
    # Simula as variáveis de ambiente do .env
    mocker.patch("os.getenv", side_effect=["teste@gmail.com", "senha_app_123"])
    
    # Simula o servidor SMTP
    mock_smtp = mocker.patch("smtplib.SMTP_SSL")
    mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
    
    send_email_notification("alvo@email.com", "Alerta de Preço", "O valor subiu!")
    
    # Verifica se fez login com as credenciais mockadas
    mock_smtp_instance.login.assert_called_once_with("teste@gmail.com", "senha_app_123")
    
    # Verifica se o e-mail foi "enviado"
    mock_smtp_instance.send_message.assert_called_once()

def test_send_email_missing_credentials(mocker):
    # Simula variáveis de ambiente vazias
    mocker.patch("os.getenv", return_value=None)
    mock_smtp = mocker.patch("smtplib.SMTP_SSL")
    
    send_email_notification("alvo@email.com", "Alerta", "Teste")
    
    # Garante que o SMTP não foi chamado se faltar credenciais
    mock_smtp.assert_not_called()