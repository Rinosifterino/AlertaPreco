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
from monitor import start_monitoring
from logger_util import log_action

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
        
        
        # Salva o nome e e-mail na classe
        self.user_name = name_input
        self.user_email = email_input
        log_action(f"Usuário Autenticado - Nome: {self.user_name} | Email: {self.user_email}")        

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
        """Inicia o loop contínuo de monitoramento em segundo plano."""
        print(f"[LOG] Monitoramento iniciado pelo usuário: {self.user_name}")
        url = self.entry_url.get().strip()
        selector = self.entry_css.get().strip() or None

        # Bloqueia a UI para indicar que está rodando
        self.save_button.configure(state="disabled", fg_color="#C0392B", text="Live Tracking Active")
        messagebox.showinfo("Monitoring Active", "O sistema está agora monitorando o leilão!")

        # Inicia o monitor.py em uma Thread (daemon=True garante que ele feche quando você fechar a janela)
        monitor_thread = threading.Thread(
            target=start_monitoring, 
            args=(url, self.user_email, 60, selector, self._update_ui_from_monitor),
            daemon=True
        )
        monitor_thread.start()

    def _update_ui_from_monitor(self, new_price: float, currency: str, prefix: str) -> None:
        """Função engatilhada pelo monitor.py para alterar os dados na tela em tempo real."""
        formatted_price = f"{new_price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        prefix_text = f"{prefix} " if prefix else ""
        new_text = f"{prefix_text}{currency} {formatted_price}"
        
        # Como vem de outra Thread, usamos .after para atualizar a interface em segurança
        self.root.after(0, self._apply_ui_update, new_text)

    def _apply_ui_update(self, new_text: str) -> None:
        """Aciona os elementos visuais na tela quando há alteração (Atendendo ao critério de avaliação)."""
        self.value_label.configure(text=f"NOVO LANCE DETECTADO: {new_text}", text_color="#E74C3C")
        self.save_button.configure(text="Price Updated! Still tracking...", fg_color="#E67E22")


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