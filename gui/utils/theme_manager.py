# banking-app/gui/utils/theme_manager.py
"""
Theme Manager for Banking Application
Handles application themes, colors, and visual styling
"""

import customtkinter as ctk
from typing import Dict, Tuple, Any
import json
import os

class ThemeManager:
    def __init__(self):
        self.current_theme = "dark"
        self.themes = self._load_themes()
        self.apply_theme(self.current_theme)
    
    def _load_themes(self) -> Dict[str, Dict[str, Any]]:
        """Load theme configurations"""
        return {
            "dark": {
                "name": "Dark",
                "appearance_mode": "dark",
                "color_theme": "blue",
                "colors": {
                    "primary": ("#1f538d", "#4dabf7"),
                    "secondary": ("#28a745", "#20c997"),
                    "danger": ("#dc3545", "#e74c3c"),
                    "warning": ("#ffc107", "#f39c12"),
                    "success": ("#28a745", "#27ae60"),
                    "info": ("#17a2b8", "#3498db"),
                    "background": ("#212529", "#2c3e50"),
                    "surface": ("#343a40", "#34495e"),
                    "text_primary": ("#ffffff", "#ecf0f1"),
                    "text_secondary": ("#adb5bd", "#bdc3c7"),
                    "border": ("#495057", "#7f8c8d"),
                    "gradient_start": ("#1a1a1a", "#2c3e50"),
                    "gradient_end": ("#2d2d2d", "#34495e")
                },
                "fonts": {
                    "heading": ("Segoe UI", 24, "bold"),
                    "subheading": ("Segoe UI", 18, "bold"),
                    "body": ("Segoe UI", 14, "normal"),
                    "small": ("Segoe UI", 12, "normal"),
                    "button": ("Segoe UI", 14, "bold")
                }
            },
            "light": {
                "name": "Light",
                "appearance_mode": "light",
                "color_theme": "blue",
                "colors": {
                    "primary": ("#0d6efd", "#0056b3"),
                    "secondary": ("#198754", "#146c43"),
                    "danger": ("#dc3545", "#b02a37"),
                    "warning": ("#fd7e14", "#e25704"),
                    "success": ("#198754", "#146c43"),
                    "info": ("#0dcaf0", "#087990"),
                    "background": ("#ffffff", "#f8f9fa"),
                    "surface": ("#f8f9fa", "#e9ecef"),
                    "text_primary": ("#212529", "#343a40"),
                    "text_secondary": ("#6c757d", "#495057"),
                    "border": ("#dee2e6", "#adb5bd"),
                    "gradient_start": ("#f8f9fa", "#ffffff"),
                    "gradient_end": ("#e9ecef", "#f1f3f4")
                },
                "fonts": {
                    "heading": ("Segoe UI", 24, "bold"),
                    "subheading": ("Segoe UI", 18, "bold"),
                    "body": ("Segoe UI", 14, "normal"),
                    "small": ("Segoe UI", 12, "normal"),
                    "button": ("Segoe UI", 14, "bold")
                }
            },
            "system": {
                "name": "System",
                "appearance_mode": "system",
                "color_theme": "blue",
                "colors": {
                    "primary": ("#1f538d", "#4dabf7"),
                    "secondary": ("#28a745", "#20c997"),
                    "danger": ("#dc3545", "#e74c3c"),
                    "warning": ("#ffc107", "#f39c12"),
                    "success": ("#28a745", "#27ae60"),
                    "info": ("#17a2b8", "#3498db"),
                    "background": ("gray90", "gray10"),
                    "surface": ("gray85", "gray15"),
                    "text_primary": ("gray10", "gray90"),
                    "text_secondary": ("gray30", "gray70"),
                    "border": ("gray60", "gray40"),
                    "gradient_start": ("gray95", "gray5"),
                    "gradient_end": ("gray80", "gray20")
                },
                "fonts": {
                    "heading": ("Segoe UI", 24, "bold"),
                    "subheading": ("Segoe UI", 18, "bold"),
                    "body": ("Segoe UI", 14, "normal"),
                    "small": ("Segoe UI", 12, "normal"),
                    "button": ("Segoe UI", 14, "bold")
                }
            }
        }
    
    def apply_theme(self, theme_name: str):
        """Apply a theme to the application"""
        if theme_name not in self.themes:
            theme_name = "dark"
        
        self.current_theme = theme_name
        theme_config = self.themes[theme_name]
        
        # Apply CustomTkinter settings
        ctk.set_appearance_mode(theme_config["appearance_mode"])
        ctk.set_default_color_theme(theme_config["color_theme"])
    
    def get_color(self, color_key: str) -> Tuple[str, str]:
        """Get color tuple for current theme"""
        theme_colors = self.themes[self.current_theme]["colors"]
        return theme_colors.get(color_key, ("#ffffff", "#000000"))
    
    def get_font(self, font_key: str) -> ctk.CTkFont:
        """Get font for current theme"""
        theme_fonts = self.themes[self.current_theme]["fonts"]
        font_config = theme_fonts.get(font_key, ("Segoe UI", 14, "normal"))
        
        return ctk.CTkFont(
            family=font_config[0],
            size=font_config[1],
            weight=font_config[2]
        )
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get list of available themes"""
        return {key: theme["name"] for key, theme in self.themes.items()}
    
    def switch_theme(self, theme_name: str):
        """Switch to a different theme"""
        if theme_name in self.themes:
            self.apply_theme(theme_name)
            return True
        return False
    
    def get_current_theme(self) -> str:
        """Get current theme name"""
        return self.current_theme
    
    def create_styled_button(self, parent, text: str, style: str = "primary", **kwargs):
        """Create a button with theme styling"""
        color = self.get_color(style)
        font = self.get_font("button")
        
        default_kwargs = {
            "text": text,
            "font": font,
            "fg_color": color,
            "corner_radius": 8,
            "height": 40
        }
        
        # Hover colors
        if style == "primary":
            default_kwargs["hover_color"] = ("#0d6efd", "#4dabf7")
        elif style == "secondary":
            default_kwargs["hover_color"] = ("#198754", "#20c997")
        elif style == "danger":
            default_kwargs["hover_color"] = ("#b02a37", "#c0392b")
        
        default_kwargs.update(kwargs)
        return ctk.CTkButton(parent, **default_kwargs)
    
    def create_styled_frame(self, parent, style: str = "surface", **kwargs):
        """Create a frame with theme styling"""
        color = self.get_color(style)
        
        default_kwargs = {
            "fg_color": color,
            "corner_radius": 10
        }
        
        default_kwargs.update(kwargs)
        return ctk.CTkFrame(parent, **default_kwargs)
    
    def create_styled_label(self, parent, text: str, style: str = "body", **kwargs):
        """Create a label with theme styling"""
        font = self.get_font(style)
        text_color = self.get_color("text_primary")
        
        default_kwargs = {
            "text": text,
            "font": font,
            "text_color": text_color
        }
        
        default_kwargs.update(kwargs)
        return ctk.CTkLabel(parent, **default_kwargs)
    
    def create_styled_entry(self, parent, placeholder: str = "", **kwargs):
        """Create an entry with theme styling"""
        font = self.get_font("body")
        
        default_kwargs = {
            "placeholder_text": placeholder,
            "font": font,
            "corner_radius": 8,
            "height": 40
        }
        
        default_kwargs.update(kwargs)
        return ctk.CTkEntry(parent, **default_kwargs)
    
    def get_banking_colors(self) -> Dict[str, Tuple[str, str]]:
        """Get banking-specific color scheme"""
        return {
            "account_balance": self.get_color("success"),
            "transaction_positive": self.get_color("success"),
            "transaction_negative": self.get_color("danger"),
            "pending_transaction": self.get_color("warning"),
            "secure_element": self.get_color("primary"),
            "error_message": self.get_color("danger"),
            "success_message": self.get_color("success"),
            "info_message": self.get_color("info")
        }
    
    def save_theme_preference(self, theme_name: str):
        """Save theme preference to file"""
        try:
            config_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(config_dir, "theme_config.json")
            
            with open(config_file, 'w') as f:
                json.dump({"current_theme": theme_name}, f)
        except Exception:
            # Silently fail if unable to save
            pass
    
    def load_theme_preference(self) -> str:
        """Load theme preference from file"""
        try:
            config_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(config_dir, "theme_config.json")
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("current_theme", "dark")
        except Exception:
            pass
        
        return "dark"