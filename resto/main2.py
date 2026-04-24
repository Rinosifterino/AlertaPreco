import os
import sys
from dotenv import load_dotenv

# Import the class and function from your new module
from resto.notifier2 import EmailNotifier, request_inputs

def main():
    """
    Função principal que orquestra a execução do sistema.
    """
    # 1. Load environment variables first
    load_dotenv()
    
    # 2. Get environment variables securely
    sender_email = os.getenv("email")
    sender_password = os.getenv("app_password")

    if not sender_email or not sender_password:
        print("[ERROR] Missing credentials in the .env file.")
        sys.exit(1)

    # 3. Request target user and email
    active_user, target_email = request_inputs()

    # 4. Initialize the Notifier
    print("\nStarting silent delivery...")
    notifier = EmailNotifier(sender_email, sender_password)
    
    # 5. Send the email (You will eventually replace the "R$ 100" with your actual scraped variables)
    notifier.send_price_alert("R$ 100", "R$ 80", target_email)

if __name__ == "__main__":
    main()