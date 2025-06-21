# banking-app/gui/components/welcome_window.py
"""
Welcome Window Component
Main landing page for the banking application
"""

import customtkinter as ctk
from typing import Dict, Callable
from ..utils.gui_utils import create_gradient_frame

class WelcomeWindow:
    def __init__(self, parent, callbacks: Dict[str, Callable]):
        self.parent = parent
        self.callbacks = callbacks
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the welcome window UI"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header()
        
        # Main content
        self.create_main_content()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Create the header section with title and branding"""
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏦 SECURE BANKING SYSTEM",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("#1f538d", "#4dabf7")
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Your trusted financial partner",
            font=ctk.CTkFont(size=16),
            text_color=("gray70", "gray30")
        )
        subtitle_label.pack(pady=(0, 20))
    
    def create_main_content(self):
        """Create the main content area with action buttons"""
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            content_frame,
            text="Welcome to your secure banking experience",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#2e2e2e", "#ffffff")
        )
        welcome_label.pack(pady=(30, 40))
        
        # Button container
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(expand=True)
        
        # Login button
        login_btn = ctk.CTkButton(
            button_frame,
            text="🔐 Login to Account",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=250,
            corner_radius=10,
            command=self.callbacks['show_login']
        )
        login_btn.pack(pady=15)
        
        # Register button
        register_btn = ctk.CTkButton(
            button_frame,
            text="📝 Create New Account",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=250,
            corner_radius=10,
            fg_color=("#28a745", "#20c997"),
            hover_color=("#218838", "#1dd1a1"),
            command=self.callbacks['show_register']
        )
        register_btn.pack(pady=15)
        
        # Exit button
        exit_btn = ctk.CTkButton(
            button_frame,
            text="❌ Exit Application",
            font=ctk.CTkFont(size=16),
            height=40,
            width=200,
            corner_radius=10,
            fg_color=("#dc3545", "#e74c3c"),
            hover_color=("#c82333", "#c0392b"),
            command=self.callbacks['exit']
        )
        exit_btn.pack(pady=(30, 15))
    
    def create_footer(self):
        """Create the footer section"""
        footer_frame = ctk.CTkFrame(self.main_frame, height=60)
        footer_frame.pack(fill="x", padx=20, pady=(10, 20))
        footer_frame.pack_propagate(False)
        
        # Security notice
        security_label = ctk.CTkLabel(
            footer_frame,
            text="🔒 Your security is our priority. All transactions are encrypted and secure.",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray40")
        )
        security_label.pack(expand=True)
        
        # Version info
        version_label = ctk.CTkLabel(
            footer_frame,
            text="Secure Banking System v2.0",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50")
        )
        version_label.pack(side="bottom", pady=(0, 5))
    
    def destroy(self):
        """Clean up the window"""
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()