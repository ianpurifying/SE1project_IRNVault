# banking_app/utils/formatters.py
"""
Formatting utilities for display
"""

from datetime import datetime
from typing import Any

class Formatters:
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format amount as currency"""
        return f"₱{amount:,.2f}"
    
    @staticmethod
    def format_account_number(account_number: str) -> str:
        """Format account number for display"""
        if len(account_number) == 10:
            return f"{account_number[:3]}-{account_number[3:6]}-{account_number[6:]}"
        return account_number
    
    @staticmethod
    def format_transaction_type(transaction_type: str) -> str:
        """Format transaction type for display"""
        type_mapping = {
            'deposit': 'Deposit',
            'withdrawal': 'Withdrawal',
            'transfer_in': 'Transfer In',
            'transfer_out': 'Transfer Out',
            'loan_disbursement': 'Loan Disbursement',
            'loan_payment': 'Loan Payment'
        }
        return type_mapping.get(transaction_type, transaction_type.title())
    
    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format datetime for display"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def format_date(dt: datetime) -> str:
        """Format date for display"""
        return dt.strftime("%Y-%m-%d")
    
    @staticmethod
    def truncate_text(text: str, max_length: int) -> str:
        """Truncate text if too long"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."