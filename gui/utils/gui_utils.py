# banking-app/gui/utils/gui_utils.py
"""
GUI Utilities Module
Common GUI helper functions and utilities for the banking application
"""

import customtkinter as ctk
from typing import Tuple, Optional
import tkinter as tk

def create_gradient_frame(parent, 
                         colors: Tuple[str, str] = ("#f0f0f0", "#e0e0e0"),
                         width: Optional[int] = None,
                         height: Optional[int] = None,
                         corner_radius: int = 10) -> ctk.CTkFrame:
    """
    Create a frame with gradient-like appearance using CustomTkinter
    
    Args:
        parent: Parent widget
        colors: Tuple of (light_color, dark_color) for light/dark mode
        width: Optional width of the frame
        height: Optional height of the frame
        corner_radius: Corner radius for the frame
    
    Returns:
        CTkFrame: Configured frame with gradient-like styling
    """
    frame = ctk.CTkFrame(
        parent,
        fg_color=colors,
        width=width,
        height=height,
        corner_radius=corner_radius
    )
    
    return frame

def create_styled_button(parent,
                        text: str,
                        command=None,
                        width: int = 200,
                        height: int = 40,
                        font_size: int = 14,
                        colors: Optional[Tuple[str, str]] = None,
                        hover_colors: Optional[Tuple[str, str]] = None) -> ctk.CTkButton:
    """
    Create a consistently styled button
    
    Args:
        parent: Parent widget
        text: Button text
        command: Command to execute on click
        width: Button width
        height: Button height
        font_size: Font size for button text
        colors: Optional custom colors (fg_color)
        hover_colors: Optional custom hover colors
    
    Returns:
        CTkButton: Styled button
    """
    button_kwargs = {
        'text': text,
        'command': command,
        'width': width,
        'height': height,
        'font': ctk.CTkFont(size=font_size, weight="bold"),
        'corner_radius': 10
    }
    
    if colors:
        button_kwargs['fg_color'] = colors
    if hover_colors:
        button_kwargs['hover_color'] = hover_colors
    
    return ctk.CTkButton(parent, **button_kwargs)

def create_entry_field(parent,
                      placeholder: str = "",
                      width: int = 250,
                      height: int = 35,
                      show_password: bool = False) -> ctk.CTkEntry:
    """
    Create a consistently styled entry field
    
    Args:
        parent: Parent widget
        placeholder: Placeholder text
        width: Entry width
        height: Entry height
        show_password: Whether to show password characters
    
    Returns:
        CTkEntry: Styled entry field
    """
    entry = ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        width=width,
        height=height,
        corner_radius=8,
        font=ctk.CTkFont(size=14)
    )
    
    if show_password:
        entry.configure(show="*")
    
    return entry

def create_label(parent,
                text: str,
                font_size: int = 14,
                font_weight: str = "normal",
                text_color: Optional[Tuple[str, str]] = None) -> ctk.CTkLabel:
    """
    Create a consistently styled label
    
    Args:
        parent: Parent widget
        text: Label text
        font_size: Font size
        font_weight: Font weight ("normal", "bold")
        text_color: Optional text color tuple for light/dark mode
    
    Returns:
        CTkLabel: Styled label
    """
    label_kwargs = {
        'text': text,
        'font': ctk.CTkFont(size=font_size, weight=font_weight)
    }
    
    if text_color:
        label_kwargs['text_color'] = text_color
    
    return ctk.CTkLabel(parent, **label_kwargs)

def center_window(window, width: int, height: int):
    """
    Center a window on the screen
    
    Args:
        window: The window to center
        width: Window width
        height: Window height
    """
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set window geometry
    window.geometry(f"{width}x{height}+{x}+{y}")

def show_message(parent, title: str, message: str, msg_type: str = "info"):
    """
    Show a message dialog
    
    Args:
        parent: Parent widget
        title: Dialog title
        message: Message text
        msg_type: Type of message ("info", "warning", "error")
    """
    import tkinter.messagebox as msgbox
    
    if msg_type == "info":
        msgbox.showinfo(title, message, parent=parent)
    elif msg_type == "warning":
        msgbox.showwarning(title, message, parent=parent)
    elif msg_type == "error":
        msgbox.showerror(title, message, parent=parent)

def validate_input(value: str, input_type: str = "text") -> bool:
    """
    Validate input based on type
    
    Args:
        value: Input value to validate
        input_type: Type of validation ("text", "email", "number", "password")
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not value or not value.strip():
        return False
    
    if input_type == "email":
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, value))
    
    elif input_type == "number":
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    elif input_type == "password":
        # Basic password validation (min 6 characters)
        return len(value) >= 6
    
    # Default text validation
    return True

def create_scrollable_frame(parent, width: int = 400, height: int = 300) -> ctk.CTkScrollableFrame:
    """
    Create a scrollable frame
    
    Args:
        parent: Parent widget
        width: Frame width
        height: Frame height
    
    Returns:
        CTkScrollableFrame: Scrollable frame
    """
    return ctk.CTkScrollableFrame(
        parent,
        width=width,
        height=height,
        corner_radius=10
    )