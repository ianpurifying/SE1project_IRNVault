# banking_app/utils/validators.py
"""
Input validation utilities
"""

import re
from typing import Optional, Tuple

class Validators:
    @staticmethod
    def validate_account_number(account_number: str) -> Tuple[bool, Optional[str]]:
        """Validate account number format"""
        if not account_number:
            return False, "Account number is required"
        
        if not account_number.isdigit():
            return False, "Account number must contain only digits"
        
        if len(account_number) != 10:
            return False, "Account number must be exactly 10 digits"
        
        return True, None
    
    @staticmethod
    def validate_amount(amount: str) -> Tuple[bool, Optional[str], Optional[float]]:
        """Validate transaction amount"""
        if not amount:
            return False, "Amount is required", None
        
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                return False, "Amount must be positive", None
            
            if amount_float > 1000000:
                return False, "Amount exceeds maximum limit", None
            
            # Check for reasonable decimal places
            if len(str(amount_float).split('.')[-1]) > 2:
                return False, "Amount can have maximum 2 decimal places", None
            
            return True, None, amount_float
            
        except ValueError:
            return False, "Invalid amount format", None
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str]]:
        """Validate user name"""
        if not name:
            return False, "Name is required"
        
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long"
        
        if len(name.strip()) > 100:
            return False, "Name cannot exceed 100 characters"
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
            return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
        
        return True, None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """Validate password strength"""
        if not password:
            return False, "Password is required"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if len(password) > 50:
            return False, "Password cannot exceed 50 characters"
        
        # Check for at least one letter and one number
        if not re.search(r'[a-zA-Z]', password):
            return False, "Password must contain at least one letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        
        return True, None
