"""
Módulo responsável pelo monitoramento contínuo de leilões.

Atualiza o estado atual em monitor.csv e registra saltos de preço em historico.csv.
"""

import csv
import os
import time
from typing import Optional, Callable

from verifier import extract_price_and_currency
from notifier import send_email_notification
from logger_util import log_action # Import do nosso log

MONITOR_CSV = "monitor.csv"
HISTORY_CSV = "historico.csv"


def start_monitoring(
    url: str,
    target_email: str,
    delay: int,
    selector: Optional[str] = None,
    ui_callback: Optional[Callable] = None
) -> None:
    print("\n[LOG] Starting monitoring loop...")

    result = extract_price_and_currency(url, selector)

    if not result:
        print("[ERROR] Could not get initial price. Halting.")
        return

    currency, original_price, prefix = result
    current_price = original_price

    print(f"[LOG] Initial price established: {prefix} {original_price} {currency}")
    
    # 1º LOG: Salva no TXT que o monitoramento começou
    log_action(f"Monitoramento Contínuo INICIADO para URL: {url} | Preço inicial: {original_price}")

    # Salva estado inicial
    _update_monitor_csv(target_email, url, original_price, current_price, currency)

    # Dispara e-mail de confirmação
    subject = "Auction Monitor: Surveillance Started"
    body = (
        f"Monitoring started for URL: {url}\n"
        f"Initial Price: {prefix} {original_price} {currency}\n\n"
        f"You will be notified when the bid increases."
    )
    send_email_notification(target_email, subject, body)

    # Loop Infinito de Monitoramento
    while True:
        print(f"\n[LOG] Waiting {delay} seconds for next check...")
        time.sleep(delay)

        result = extract_price_and_currency(url, selector)

        if not result:
            print("[LOG] Failed to fetch new price in this cycle.")
            continue

        # É AQUI que a variável new_price é criada
        new_currency, new_price, new_prefix = result
        print(f"[LOG] Fetched current price: {new_prefix} {new_price} {new_currency}")

        # Lógica de Leilão: Só alerta e salva se o valor AUMENTAR
        if new_price > current_price and _is_valid_variation(current_price, new_price):
            print("[LOG] Valid price INCREASE detected!")
            
            # 2º LOG: Agora sim a variável new_price existe e podemos logar a mudança!
            log_action(f"MUDANÇA DETECTADA! Valor subiu de {current_price} para {new_price} na URL: {url}")

            # 1. Salva os dois valores no histórico
            _append_history_csv(url, current_price, new_price, currency)

            # 2. Envia o e-mail de ALERTA
            alert_subject = "Price Increase Alert: Auction Monitor"
            alert_body = (
                f"The bid has increased!\n\n"
                f"Previous Value: {current_price} {currency}\n"
                f"New Value: {new_price} {new_currency}\n\n"
                f"Link: {url}"
            )
            send_email_notification(target_email, alert_subject, alert_body)

            # 3. Avisa a UI para atualizar o número na tela
            if ui_callback:
                ui_callback(new_price, new_currency, new_prefix)

            # 4. Atualiza o estado atual no monitor principal
            current_price = new_price
            _update_monitor_csv(target_email, url, original_price, current_price, currency)


def _is_valid_variation(old_price: float, new_price: float) -> bool:
    """Filtro de segurança para descartar anomalias de captura."""
    if new_price > (old_price * 10.0):
        print(f"[WARNING] Ignoring suspicious spike to {new_price}")
        return False
    return True


def _update_monitor_csv(email: str, url: str, original_price: float, current_price: float, currency: str) -> None:
    """Atualiza o arquivo monitor.csv sobrescrevendo o arquivo."""
    try:
        with open(MONITOR_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["email", "url", "original_price", "current_price", "currency"])
            writer.writerow([email, url, original_price, current_price, currency])
        print("[LOG] monitor.csv updated with latest price.")
    except Exception as error:
        print(f"[ERROR] Failed to update {MONITOR_CSV}: {error}")


def _append_history_csv(url: str, old_price: float, new_price: float, currency: str) -> None:
    """Registra exclusivamente as mudanças de preço (saltos) no historico.csv."""
    try:
        file_exists = os.path.isfile(HISTORY_CSV)
        with open(HISTORY_CSV, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["url", "old_price", "new_price", "currency"])
            writer.writerow([url, old_price, new_price, currency])
        print("[LOG] Price jump recorded in historico.csv.")
    except Exception as error:
        print(f"[ERROR] Failed to write to {HISTORY_CSV}: {error}")