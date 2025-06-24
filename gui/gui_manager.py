# banking-app/gui/gui_manager.py:
import customtkinter as ctk
from typing import Optional, Dict, Any, Callable
from .components.welcome_window import WelcomeWindow
from .components.user_dashboard import UserDashboard
from .components.admin_dashboard import AdminDashboard
from .components.login_window import LoginWindow
from .components.register_window import RegisterWindow
from .utils.theme_manager import ThemeManager
from .utils.gui_utils import center_window

class GUIManager:
    def __init__(self, banking_app_instance):
        self.banking_app = banking_app_instance
        self.root = None
        self.current_window = None
        self.theme_manager = ThemeManager()
        
        # Initialize CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
    def start(self):
        """Start the GUI application"""
        self.root = ctk.CTk()
        self.root.title("IRN Vault Banking System")
        self.root.geometry("800x600")
        center_window(self.root, 800, 600)
        
        # Set window icon and properties
        self.root.resizable(True, True)
        self.root.minsize(600, 400)
        
        # Initialize with welcome window
        self.show_welcome_window()
        
        # Start the main loop
        self.root.mainloop()
    
    def show_welcome_window(self):
        """Display the welcome/main menu window"""
        self._clear_current_window()
        self.current_window = WelcomeWindow(
            self.root, 
            self._get_callbacks()
        )
    
    def show_login_window(self):
        """Display the login window"""
        self._clear_current_window()
        self.current_window = LoginWindow(
            self.root,
            self._get_callbacks(),
            self.banking_app.auth_service
        )
    
    def show_register_window(self):
        """Display the registration window"""
        self._clear_current_window()
        self.current_window = RegisterWindow(
            self.root,
            self._get_callbacks(),
            self.banking_app.auth_service
        )
    
    def show_user_dashboard(self, user_data: Dict[str, Any]):
        """Display the user dashboard"""
        self._clear_current_window()
        self.current_window = UserDashboard(
            self.root,
            self._get_callbacks(),
            user_data,
            {
                'transaction_service': self.banking_app.transaction_service,
                'user_service': self.banking_app.user_service,
                'statement_service': self.banking_app.statement_service,
                'loan_service': self.banking_app.loan_service  
            }
        )
    
    def show_admin_dashboard(self, admin_data: Dict[str, Any]):
        """Display the admin dashboard"""
        self._clear_current_window()
        self.current_window = AdminDashboard(
            self.root,
            self._get_callbacks(),
            admin_data,
            self.banking_app.admin_service
        )
    
    def logout(self):
        """Handle logout and return to welcome screen"""
        self.banking_app.current_user = None
        self.banking_app.is_admin = False
        self.show_welcome_window()
    
    def exit_application(self):
        """Safely exit the application"""
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def _clear_current_window(self):
        """Clear the current window content"""
        if self.current_window:
            self.current_window.destroy()
            self.current_window = None
        
        # Clear all widgets from root
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def _get_callbacks(self) -> Dict[str, Callable]:
        """Get dictionary of callback functions for GUI components"""
        return {
            'show_welcome': self.show_welcome_window,
            'show_login': self.show_login_window,
            'show_register': self.show_register_window,
            'show_user_dashboard': self.show_user_dashboard,
            'show_admin_dashboard': self.show_admin_dashboard,
            'logout': self.logout,
            'exit': self.exit_application,
            'login_user': self._handle_login,
            'register_user': self._handle_registration
        }
    
    def _handle_login(self, account_number: str, password: str) -> tuple[bool, str, Optional[Dict]]:
        """Handle login attempt"""
        try:
            user = self.banking_app.auth_service.login(account_number, password)
            self.banking_app.current_user = user
            self.banking_app.is_admin = account_number == '0000000001'
            
            if self.banking_app.is_admin:
                self.show_admin_dashboard(user)
            else:
                self.show_user_dashboard(user)
                
            return True, "Login successful!", user
            
        except Exception as e:
            return False, str(e), None
    
    def _handle_registration(self, name: str, password: str) -> tuple[bool, str, Optional[str]]:
        """Handle registration attempt"""
        try:
            account_number = self.banking_app.auth_service.register_user(name, password)
            return True, f"Registration successful! Account number: {account_number}", account_number
        except Exception as e:
            return False, str(e), None