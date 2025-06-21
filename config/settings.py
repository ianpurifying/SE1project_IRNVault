# banking_app/config/settings.py
"""
Application configuration settings
"""

import os
from typing import Dict, Any

class Settings:
    # Database configuration
    DATABASE_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'se1project'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', 3306)),
    }
    
    # Security settings
    MIN_PASSWORD_LENGTH = 6
    ADMIN_ACCOUNT_NUMBER = '0000000001'
    
    # Transaction limits
    MAX_TRANSACTION_AMOUNT = 1000000.00
    MIN_TRANSACTION_AMOUNT = 0.01
    
    # Application settings
    APP_NAME = "Secure Banking System"
    APP_VERSION = "1.0.0"
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'banking_app.log')
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """Get database configuration"""
        return cls.DATABASE_CONFIG.copy()
    
    @classmethod
    def is_admin_account(cls, account_number: str) -> bool:
        """Check if account number is admin account"""
        return account_number == cls.ADMIN_ACCOUNT_NUMBER