"""
Modern and Organized User Interface module for the Auction Monitor application.

This module provides a graphical user interface using CustomTkinter.
It integrates with the verifier and notifier modules.
"""

import re
import threading
import customtkinter as ctk
from tkinter import messagebox

# Importações dos seus módulos (precisam estar na mesma pasta)
from verifier import extract_price_and_currency
from notifier import send_email_notification

# =============================================================================
# CONSTANTS
# =============================================================================
WINDOW_TITLE = "Auction Monitor Pro"
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 600
EMAIL_REGEX_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# UI Theme Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =============================================================================
# MAIN APPLICATION CLASS
# =============================================================================
class AuctionApp:
    """
    Main application class for the modern Auction Monitor GUI.
    """

    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        # Variáveis para guardar os dados do usuário logado
        self.user_name = ""
        self.user_email = ""
        self.current_price_text = ""
        
        self._setup_window()
        self._build_login_screen()

    # -------------------------------------------------------------------------
    # SETUP & CONFIGURATION METHODS
    # -------------------------------------------------------------------------
    def _setup_window(self) -> None:
        """Configure the main window properties and center it on the screen."""
        self.root.title(WINDOW_TITLE)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (WINDOW_WIDTH / 2))
        y_coordinate = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")
        self.root.resizable(False, False)

    # -------------------------------------------------------------------------
    # LOGIN SCREEN
    # -------------------------------------------------------------------------
    def _build_login_screen(self) -> None:
        """Construct and display the modern login interface."""
        self.login_frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.login_frame.pack(pady=70, padx=60, fill="both", expand=True)

        ctk.CTkLabel(
            self.login_frame, text="Welcome to Monitor Pro", font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(40, 30))

        # Name Field
        ctk.CTkLabel(self.login_frame, text="Nome Completo", font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", padx=65)
        self.entry_name = ctk.CTkEntry(self.login_frame, placeholder_text="escreva seu nome aqui", width=280, height=40)
        self.entry_name.pack(pady=(0, 15))

        # Email Field
        ctk.CTkLabel(self.login_frame, text="Endereço de E-mail", font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", padx=65)
        self.entry_email = ctk.CTkEntry(self.login_frame, placeholder_text="insira seu email válido aqui", width=280, height=40)
        self.entry_email.pack(pady=(0, 25))

        # Login Button
        ctk.CTkButton(
            self.login_frame, text="Access System", command=self._validate_login, width=280, height=45, corner_radius=8, font=ctk.CTkFont(size=15, weight="bold")
        ).pack(pady=(10, 30))

    def _validate_login(self) -> None:
        """Validate credentials and save user data."""
        name_input = self.entry_name.get().strip()
        email_input = self.entry_email.get().strip()
        name_without_spaces = name_input.replace(" ", "")

        if len(name_input) < 3 or not name_without_spaces.isalpha():
            messagebox.showerror("Validation Error", "Name must be at least 3 characters long and contain only letters.")
            return
        
        if not re.match(EMAIL_REGEX_PATTERN, email_input):
            messagebox.showerror("Validation Error", "Please enter a valid email address (e.g., user@domain.com).")
            return

        # Salva o nome e e-mail na classe para usarmos depois no envio
        self.user_name = name_input
        self.user_email = email_input

        print(f"[LOG] Usuário logado: {self.user_name} - Email: {self.user_email}")
        self.login_frame.destroy()
        self._build_monitoring_screen()

    # -------------------------------------------------------------------------
    # MONITORING SCREEN
    # -------------------------------------------------------------------------
    def _build_monitoring_screen(self) -> None:
        """Construct and display the main auction monitoring interface."""
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.main_frame.pack(pady=50, padx=40, fill="both", expand=True)

        ctk.CTkLabel(
            self.main_frame, text="Configure Target", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(30, 20))

        # URL Input
        ctk.CTkLabel(self.main_frame, text="Target Auction URL:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=50)
        self.entry_url = ctk.CTkEntry(self.main_frame, placeholder_text="https://...", width=350, height=40)
        self.entry_url.pack(pady=(5, 20))

        # CSS Input
        ctk.CTkLabel(self.main_frame, text="Element CSS Selector (Opcional):", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=50)
        self.entry_css = ctk.CTkEntry(self.main_frame, placeholder_text="e.g., .price-tag", width=350, height=40)
        self.entry_css.pack(pady=(5, 30))

        # Fetch Button
        self.fetch_button = ctk.CTkButton(
            self.main_frame, text="Test & Fetch Value", command=self._start_fetch_thread, width=250, height=40, font=ctk.CTkFont(weight="bold")
        )
        self.fetch_button.pack(pady=10)

        # Result Area
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.value_label = ctk.CTkLabel(self.result_frame, text="", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2FA572")
        self.save_button = ctk.CTkButton(
            self.result_frame, text="Confirm & Start Monitoring", command=self._save_value, fg_color="#2FA572", hover_color="#1F7A50", width=250, height=40, font=ctk.CTkFont(weight="bold")
        )

    def _start_fetch_thread(self) -> None:
        url = self.entry_url.get().strip()
        selector = self.entry_css.get().strip() or None
        
        if not url.startswith("http"):
            messagebox.showwarning("URL Inválida", "Por favor, insira uma URL válida começando com http ou https.")
            return

        self.fetch_button.configure(state="disabled", text="Buscando no site...")
        self.result_frame.pack_forget()
        
        thread = threading.Thread(target=self._run_extraction_task, args=(url, selector))
        thread.start()

    def _run_extraction_task(self, url: str, selector: str) -> None:
        result = extract_price_and_currency(url, selector)
        self.root.after(0, self._handle_extraction_result, result)

    def _handle_extraction_result(self, result) -> None:
        self.fetch_button.configure(state="normal", text="Test & Fetch Value")

        if result:
            currency, price, prefix = result
            formatted_price = f"{price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            prefix_text = f"{prefix} " if prefix else ""
            
            # Salva o texto formatado para colocar no e-mail depois
            self.current_price_text = f"{prefix_text}{currency} {formatted_price}"
            
            self.result_frame.pack(pady=20, fill="x")
            self.value_label.configure(text=f"Valor Encontrado: {self.current_price_text}")
            self.value_label.pack(pady=(0, 15))
            self.save_button.pack()
            self.save_button.configure(state="normal", text="Confirm & Start Monitoring", fg_color="#2FA572")
        else:
            messagebox.showerror("Falha na Extração", "Não foi possível encontrar um valor válido na página.")

    def _save_value(self) -> None:
        """Inicia o monitoramento e dispara o e-mail em segundo plano."""
        print(f"[LOG] Monitoramento iniciado pelo usuário: {self.user_name}")
        url = self.entry_url.get().strip()

        # Inicia a thread de disparo do e-mail
        email_thread = threading.Thread(target=self._send_confirmation_email, args=(url,))
        email_thread.start()

        messagebox.showinfo("Monitoring Active", "Configuration saved! Check your email for confirmation.")
        self.save_button.configure(state="disabled", fg_color="gray", text="Monitoring...")

    def _send_confirmation_email(self, url: str) -> None:
        """Monta e dispara o e-mail."""
        subject = "Confirmação de Monitoramento - Auction Monitor Pro"
        body = (f"Olá, {self.user_name}!\n\n"
                f"Seu monitoramento foi iniciado com sucesso.\n\n"
                f"URL Monitorada: {url}\n"
                f"Valor Atual Encontrado: {self.current_price_text}\n\n"
                f"O sistema irá notificá-lo caso ocorram mudanças.\n"
                f"Equipe Auction Monitor Pro")
        
        # Chama o seu arquivo notifier.py passando os dados do usuário atual
        send_email_notification(self.user_email, subject, body)


# =============================================================================
# EXECUTION
# =============================================================================
if __name__ == "__main__":
    # Tenta carregar as variáveis do arquivo .env (caso você use a biblioteca python-dotenv)
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    app_window = ctk.CTk()
    application = AuctionApp(app_window)
    app_window.mainloop()