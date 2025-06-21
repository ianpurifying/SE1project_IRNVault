# banking-app/gui/components/login_window.py
"""
Login Window Component
Handles user authentication
"""

import customtkinter as ctk
from typing import Dict, Callable
import tkinter.messagebox as messagebox

class LoginWindow:
    def __init__(self, parent, callbacks: Dict[str, Callable], auth_service):
        self.parent = parent
        self.callbacks = callbacks
        self.auth_service = auth_service
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the login window UI"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Create login form
        self.create_login_form()
    
    def create_login_form(self):
        """Create the login form"""
        # Header
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            width=80,
            height=30,
            font=ctk.CTkFont(size=12),
            command=self.callbacks['show_welcome']
        )
        back_btn.pack(anchor="w", padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔐 Account Login",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1f538d", "#4dabf7")
        )
        title_label.pack(pady=(10, 20))
        
        # Form container
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Center the form
        center_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        center_frame.pack(expand=True)
        
        # Account number field
        account_label = ctk.CTkLabel(
            center_frame,
            text="Account Number:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        account_label.pack(pady=(40, 5))
        
        self.account_entry = ctk.CTkEntry(
            center_frame,
            placeholder_text="Enter 10-digit account number",
            font=ctk.CTkFont(size=14),
            height=40,
            width=300
        )
        self.account_entry.pack(pady=(0, 20))
        
        # Password field
        password_label = ctk.CTkLabel(
            center_frame,
            text="Password:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        password_label.pack(pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            center_frame,
            placeholder_text="Enter 6-digit password",
            font=ctk.CTkFont(size=14),
            height=40,
            width=300,
            show="*"
        )
        self.password_entry.pack(pady=(0, 30))
        
        # Login button
        login_btn = ctk.CTkButton(
            center_frame,
            text="🔓 Login",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=200,
            corner_radius=10,
            command=self.handle_login
        )
        login_btn.pack(pady=10)
        
        # Additional options
        options_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        options_frame.pack(pady=20)
        
        # Register link
        register_label = ctk.CTkLabel(
            options_frame,
            text="Don't have an account?",
            font=ctk.CTkFont(size=12)
        )
        register_label.pack()
        
        register_btn = ctk.CTkButton(
            options_frame,
            text="Create New Account",
            font=ctk.CTkFont(size=12),
            height=30,
            width=150,
            fg_color="transparent",
            text_color=("#1f538d", "#4dabf7"),
            hover_color=("gray80", "gray20"),
            command=self.callbacks['show_register']
        )
        register_btn.pack(pady=5)
        
        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda event: self.handle_login())
        self.account_entry.bind("<Return>", lambda event: self.password_entry.focus())
        
        # Focus on account entry
        self.account_entry.focus()
    
    def handle_login(self):
        """Handle login attempt"""
        account_number = self.account_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validation
        if not account_number:
            messagebox.showerror("Login Error", "Please enter your account number.")
            self.account_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Login Error", "Please enter your password.")
            self.password_entry.focus()
            return
        
        if len(account_number) != 10 or not account_number.isdigit():
            messagebox.showerror("Login Error", "Account number must be exactly 10 digits.")
            self.account_entry.focus()
            return
        
        if len(password) != 6 or not password.isdigit():
            messagebox.showerror("Login Error", "Password must be exactly 6 digits.")
            self.password_entry.focus()
            return
        
        # Attempt login
        success, message, user_data = self.callbacks['login_user'](account_number, password)
        
        if success:
            messagebox.showinfo("Login Successful", message)
        else:
            messagebox.showerror("Login Failed", message)
            # Clear password field
            self.password_entry.delete(0, 'end')
            self.password_entry.focus()
    
    def destroy(self):
        """Clean up the window"""
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()