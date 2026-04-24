import datetime

LOG_FILE = "log.txt"

def log_action(message: str) -> None:
    """
    Registra uma mensagem no arquivo log.txt com timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
        # Também imprime no console para você ver enquanto testa
        print(f"[LOG_FILE] {message}")
    except Exception as e:
        print(f"[ERROR] Falha ao escrever no log: {e}")