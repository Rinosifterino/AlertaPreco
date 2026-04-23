"""
Modern and Organized User Interface module for the Auction Monitor application.

This module provides a graphical user interface using CustomTkinter.
It enforces PEP8 styling, proper naming conventions, and PEP257 docstrings.
"""

import customtkinter as ctk
from tkinter import messagebox

# =============================================================================
# CONSTANTS
# =============================================================================
WINDOW_TITLE = "Auction Monitor Pro"
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 650
MOCK_FETCHED_PRICE = "R$ 150,00"

# UI Theme Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =============================================================================
# MAIN APPLICATION CLASS
# =============================================================================
class AuctionApp:
    """
    Main application class for the modern Auction Monitor GUI.
    
    Handles window management, state variables, and view rendering 
    for both the Login and Monitoring screens.
    """

    def __init__(self, root: ctk.CTk) -> None:
        """
        Initialize the application, setup the window, and load the first screen.

        Args:
            root (ctk.CTk): The main CustomTkinter root window.
        """
        self.root = root
        
        self._setup_window()
        self._initialize_variables()
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

    def _initialize_variables(self) -> None:
        """Initialize all Tkinter variables used to store user input."""
        self.user_name = ctk.StringVar()
        self.user_email = ctk.StringVar()
        self.auction_url = ctk.StringVar()
        self.css_selector = ctk.StringVar()

    # -------------------------------------------------------------------------
    # LOGIN SCREEN
    # -------------------------------------------------------------------------
    def _build_login_screen(self) -> None:
        """Construct and display the modern login interface."""
        self.login_frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.login_frame.pack(pady=100, padx=60, fill="both", expand=True)

        # Header
        ctk.CTkLabel(
            self.login_frame, 
            text="Welcome to Monitor Pro", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(50, 30))

        # Input Fields
        ctk.CTkEntry(
            self.login_frame, 
            textvariable=self.user_name, 
            placeholder_text="Enter your full name",
            width=280,
            height=45
        ).pack(pady=10)

        ctk.CTkEntry(
            self.login_frame, 
            textvariable=self.user_email, 
            placeholder_text="Enter your email address",
            width=280,
            height=45
        ).pack(pady=10)

        # Login Button
        ctk.CTkButton(
            self.login_frame, 
            text="Access System", 
            command=self._validate_login,
            width=280,
            height=45,
            corner_radius=8,
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(pady=(30, 50))

    def _validate_login(self) -> None:
        """
        Validate the login credentials based on strict business rules.
        Requires name to be >= 3 chars and contain only letters.
        """
        name_input = self.user_name.get().strip()
        email_input = self.user_email.get().strip()
        name_without_spaces = name_input.replace(" ", "")

        # Validation logic
        if len(name_input) < 3 or not name_without_spaces.isalpha():
            messagebox.showerror(
                "Validation Error", 
                "Name must be at least 3 characters long and contain only letters."
            )
            return
        
        if not email_input:
            messagebox.showerror("Validation Error", "Email cannot be empty.")
            return

        # Transition to main screen
        messagebox.showinfo("Success", f"Welcome, {name_input}!")
        self.login_frame.destroy()
        self._build_monitoring_screen()

    # -------------------------------------------------------------------------
    # MONITORING SCREEN
    # -------------------------------------------------------------------------
    def _build_monitoring_screen(self) -> None:
        """Construct and display the main auction monitoring interface."""
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.main_frame.pack(pady=50, padx=40, fill="both", expand=True)

        # Header
        ctk.CTkLabel(
            self.main_frame, 
            text="Configure Target", 
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(30, 20))

        # URL Input
        ctk.CTkLabel(self.main_frame, text="Target Auction URL:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=50)
        ctk.CTkEntry(
            self.main_frame, 
            textvariable=self.auction_url, 
            placeholder_text="https://...",
            width=350,
            height=40
        ).pack(pady=(5, 20))

        # CSS Selector Input
        ctk.CTkLabel(self.main_frame, text="Element CSS Selector:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=50)
        ctk.CTkEntry(
            self.main_frame, 
            textvariable=self.css_selector, 
            placeholder_text="e.g., .price-tag, #current-bid",
            width=350,
            height=40
        ).pack(pady=(5, 30))

        # Fetch Button
        ctk.CTkButton(
            self.main_frame, 
            text="Test & Fetch Value", 
            command=self._fetch_auction_value,
            width=250,
            height=40,
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=10)

        # Result Area (Hidden initially)
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        self.value_label = ctk.CTkLabel(
            self.result_frame, 
            text="", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2FA572"
        )
        
        self.save_button = ctk.CTkButton(
            self.result_frame, 
            text="Confirm & Start Monitoring", 
            command=self._save_value, 
            fg_color="#2FA572",
            hover_color="#1F7A50",
            width=250,
            height=40,
            font=ctk.CTkFont(weight="bold")
        )

    def _fetch_auction_value(self) -> None:
        """Simulate the scraping process and display the result for confirmation."""
        url = self.auction_url.get().strip()
        selector = self.css_selector.get().strip()

        if not url or not selector:
            messagebox.showwarning("Missing Data", "Please provide both URL and CSS Selector.")
            return

        # Display result elements
        self.result_frame.pack(pady=20, fill="x")
        self.value_label.configure(text=f"Current Value: {MOCK_FETCHED_PRICE}")
        self.value_label.pack(pady=(0, 15))
        self.save_button.pack()

    def _save_value(self) -> None:
        """Persist the configuration and lock the UI state to indicate monitoring."""
        messagebox.showinfo("Monitoring Active", "Configuration saved! The tracker is now running.")
        self.save_button.configure(state="disabled", fg_color="gray", text="Monitoring...")


# =============================================================================
# EXECUTION
# =============================================================================
if __name__ == "__main__":
    app_window = ctk.CTk()
    application = AuctionApp(app_window)
    app_window.mainloop()