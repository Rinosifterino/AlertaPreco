"""
Módulo responsável pelo monitoramento contínuo de leilões.

Atualiza o estado atual em monitor.csv e registra saltos de preço em historico.csv.
"""

import csv
import os
import time
from typing import Optional

from verifier import extract_price_and_currency
from resto.notifier2 import send_email_notification

MONITOR_CSV = "monitor.csv"
HISTORY_CSV = "historico.csv"


def start_monitoring(
    url: str,
    target_email: str,
    delay: int,
    selector: Optional[str] = None
) -> None:
    """
    Inicia o loop principal de monitoramento.
    
    :param url: URL do produto.
    :param target_email: Email para receber os alertas.
    :param delay: Tempo de espera entre checagens (em segundos).
    :param selector: Opcional, seletor CSS/XPath para forçar a busca num local.
    """
    print("\n[LOG] Starting monitoring loop...")

    result = extract_price_and_currency(url, selector)

    if not result:
        print("[ERROR] Could not get initial price. Halting.")
        return

    original_price, currency, prefix = result
    current_price = original_price

    print(f"[LOG] Initial price established: {prefix} {original_price} {currency}")

    # Salva estado inicial
    _update_monitor_csv(target_email, url, original_price, current_price, currency)

    # Dispara e-mail de confirmação
    subject = "Auction Monitor: Surveillance Started"
    body = (
        f"Monitoring started for URL: {url}\n"
        f"Initial Price: {prefix} {original_price} {currency}\n\n"
        "You will be notified when the bid increases."
    )
    send_email_notification(target_email, subject, body)

    while True:
        print(f"\n[LOG] Waiting {delay} seconds for next check...")
        time.sleep(delay)

        result = extract_price_and_currency(url, selector)

        if not result:
            print("[LOG] Failed to fetch new price in this cycle.")
            continue

        new_price, new_currency, new_prefix = result
        print(f"[LOG] Fetched current price: {new_prefix} {new_price} {new_currency}")

        # Lógica de Leilão: Só alerta e salva se o valor AUMENTAR
        if new_price > current_price and _is_valid_variation(current_price, new_price):
            print("[LOG] Valid price INCREASE detected!")

            # Salva os dois valores no histórico
            _append_history_csv(url, current_price, new_price, currency)

            # Envia o e-mail
            alert_subject = "Price Increase Alert: Auction Monitor"
            alert_body = (
                f"The bid has increased!\n\n"
                f"Previous Value: {current_price} {currency}\n"
                f"New Value: {new_price} {new_currency}\n\n"
                f"Link: {url}"
            )
            send_email_notification(target_email, alert_subject, alert_body)

            # Atualiza o estado atual no monitor principal
            current_price = new_price
            _update_monitor_csv(target_email, url, original_price, current_price, currency)


def _is_valid_variation(old_price: float, new_price: float) -> bool:
    """
    Filtro de segurança para descartar anomalias de captura (ex: pulou para um valor 10x maior por bug HTML).
    """
    if new_price > (old_price * 10.0):
        print(f"[WARNING] Ignoring suspicious spike to {new_price}")
        return False
    return True


def _update_monitor_csv(
    email: str, url: str, original_price: float, current_price: float, currency: str
) -> None:
    """
    Atualiza o arquivo monitor.csv.
    Modo 'w' sobrescreve o arquivo garantindo que apenas o último valor lido esteja lá.
    """
    try:
        with open(MONITOR_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["email", "url", "original_price", "current_price", "currency"])
            writer.writerow([email, url, original_price, current_price, currency])
        print("[LOG] monitor.csv updated with latest price.")
    except Exception as error:
        print(f"[ERROR] Failed to update {MONITOR_CSV}: {error}")


def _append_history_csv(url: str, old_price: float, new_price: float, currency: str) -> None:
    """
    Registra exclusivamente as mudanças de preço (saltos) no historico.csv.
    """
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