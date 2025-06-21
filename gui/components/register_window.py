# banking-app/gui/components/register_window.py
"""
Registration Window Component
Handles new user registration
"""

import customtkinter as ctk
from typing import Dict, Callable
import tkinter.messagebox as messagebox

class RegisterWindow:
    def __init__(self, parent, callbacks: Dict[str, Callable], auth_service):
        self.parent = parent
        self.callbacks = callbacks
        self.auth_service = auth_service
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the registration window UI"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Create registration form
        self.create_registration_form()
    
    def create_registration_form(self):
        """Create the registration form"""
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
            text="📝 Create New Account",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#28a745", "#20c997")
        )
        title_label.pack(pady=(10, 20))
        
        # Form container
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Center the form
        center_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        center_frame.pack(expand=True)
        
        # Full name field
        name_label = ctk.CTkLabel(
            center_frame,
            text="Full Name:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack(pady=(30, 5))
        
        self.name_entry = ctk.CTkEntry(
            center_frame,
            placeholder_text="Enter your full name",
            font=ctk.CTkFont(size=14),
            height=40,
            width=300
        )
        self.name_entry.pack(pady=(0, 15))
        
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
        self.password_entry.pack(pady=(0, 15))
        
        # Confirm password field
        confirm_label = ctk.CTkLabel(
            center_frame,
            text="Confirm Password:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        confirm_label.pack(pady=(0, 5))
        
        self.confirm_entry = ctk.CTkEntry(
            center_frame,
            placeholder_text="Confirm your password",
            font=ctk.CTkFont(size=14),
            height=40,
            width=300,
            show="*"
        )
        self.confirm_entry.pack(pady=(0, 25))
        
        # Password requirements
        req_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        req_frame.pack(pady=(0, 20))
        
        req_label = ctk.CTkLabel(
            req_frame,
            text="Password Requirements:\n• Exactly 6 digits\n• Numeric characters only",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray40"),
            justify="left"
        )
        req_label.pack()
        
        # Register button
        register_btn = ctk.CTkButton(
            center_frame,
            text="✓ Create Account",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=200,
            corner_radius=10,
            fg_color=("#28a745", "#20c997"),
            hover_color=("#218838", "#1dd1a1"),
            command=self.handle_registration
        )
        register_btn.pack(pady=15)
        
        # Login link
        login_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        login_frame.pack(pady=15)
        
        login_label = ctk.CTkLabel(
            login_frame,
            text="Already have an account?",
            font=ctk.CTkFont(size=12)
        )
        login_label.pack()
        
        login_btn = ctk.CTkButton(
            login_frame,
            text="Login Here",
            font=ctk.CTkFont(size=12),
            height=30,
            width=120,
            fg_color="transparent",
            text_color=("#1f538d", "#4dabf7"),
            hover_color=("gray80", "gray20"),
            command=self.callbacks['show_login']
        )
        login_btn.pack(pady=5)
        
        # Bind Enter key
        self.confirm_entry.bind("<Return>", lambda event: self.handle_registration())
        
        # Focus on name entry
        self.name_entry.focus()
    
    def handle_registration(self):
        """Handle registration attempt"""
        name = self.name_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_entry.get().strip()
        
        # Validation
        if not name:
            messagebox.showerror("Registration Error", "Please enter your full name.")
            self.name_entry.focus()
            return
        
        if len(name) < 2:
            messagebox.showerror("Registration Error", "Name must be at least 2 characters long.")
            self.name_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Registration Error", "Please enter a password.")
            self.password_entry.focus()
            return
        
        if len(password) != 6 or not password.isdigit():
            messagebox.showerror("Registration Error", "Password must be exactly 6 digits.")
            self.password_entry.focus()
            return
        
        if not confirm_password:
            messagebox.showerror("Registration Error", "Please confirm your password.")
            self.confirm_entry.focus()
            return
        
        if password != confirm_password:
            messagebox.showerror("Registration Error", "Passwords do not match.")
            self.confirm_entry.delete(0, 'end')
            self.confirm_entry.focus()
            return
        
        # Attempt registration
        success, message, account_number = self.callbacks['register_user'](name, password)
        
        if success:
            # Show success message with account number
            result = messagebox.showinfo(
                "Registration Successful", 
                f"{message}\n\nYour account is pending approval.\nPlease wait for admin approval to login."
            )
            # Return to welcome screen
            self.callbacks['show_welcome']()
        else:
            messagebox.showerror("Registration Failed", message)
            # Clear password fields
            self.password_entry.delete(0, 'end')
            self.confirm_entry.delete(0, 'end')
            self.password_entry.focus()
    
    def destroy(self):
        """Clean up the window"""
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()