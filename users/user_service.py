# banking_app/users/user_service.py
"""
User service
Handles user account management and operations
"""

from typing import Optional, Dict, Any, List
from db.database import Database

class UserService:
    def __init__(self, database: Database):
        self.db = database

    def get_user_by_account(self, account_number: str) -> Optional[Dict[str, Any]]:
        """Get user by account number"""
        query = "SELECT * FROM accounts WHERE account_number = %s"
        user = self.db.fetch_one(query, (account_number,))
        
        if user:
            return {
                'account_number': user['account_number'],
                'name': user['name'],
                'balance': float(user['balance']),
                'is_approved': user['is_approved'],
                'created_at': user['created_at']
            }
        return None

    def update_balance(self, account_number: str, new_balance: float) -> bool:
        """Update user balance"""
        query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
        return self.db.execute_query(query, (new_balance, account_number))

    def get_balance(self, account_number: str) -> Optional[float]:
        """Get current balance for account"""
        query = "SELECT balance FROM accounts WHERE account_number = %s"
        result = self.db.fetch_one(query, (account_number,))
        return float(result['balance']) if result else None

    def account_exists(self, account_number: str) -> bool:
        """Check if account exists"""
        query = "SELECT 1 FROM accounts WHERE account_number = %s"
        return self.db.fetch_one(query, (account_number,)) is not None

    def is_account_approved(self, account_number: str) -> bool:
        """Check if account is approved"""
        query = "SELECT is_approved FROM accounts WHERE account_number = %s"
        result = self.db.fetch_one(query, (account_number,))
        return result['is_approved'] if result else False

    def get_user_profile(self, account_number: str) -> Optional[Dict[str, Any]]:
        """Get complete user profile"""
        user = self.get_user_by_account(account_number)
        if not user:
            return None
        
        # Get transaction count
        query = "SELECT COUNT(*) as transaction_count FROM transactions WHERE account_number = %s"
        result = self.db.fetch_one(query, (account_number,))
        user['transaction_count'] = result['transaction_count'] if result else 0
        
        return user

    def search_users(self, search_term: str) -> List[Dict[str, Any]]:
        """Search users by name"""
        query = """
            SELECT account_number, name, balance, is_approved, created_at 
            FROM accounts 
            WHERE name LIKE %s AND account_number != '0000000001'
            ORDER BY name
        """
        results = self.db.fetch_all(query, (f"%{search_term}%",))
        
        return [{
            'account_number': row['account_number'],
            'name': row['name'],
            'balance': float(row['balance']),
            'is_approved': row['is_approved'],
            'created_at': row['created_at']
        } for row in results]

    def get_account_summary(self, account_number: str) -> Optional[Dict[str, Any]]:
        """Get account summary with transaction statistics"""
        user = self.get_user_by_account(account_number)
        if not user:
            return None
        
        # Get transaction statistics
        query = """
            SELECT 
                COUNT(*) as total_transactions,
                SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END) as total_deposits,
                SUM(CASE WHEN type = 'withdrawal' THEN amount ELSE 0 END) as total_withdrawals,
                SUM(CASE WHEN type = 'transfer_out' THEN amount ELSE 0 END) as total_transfers_out,
                SUM(CASE WHEN type = 'transfer_in' THEN amount ELSE 0 END) as total_transfers_in
            FROM transactions 
            WHERE account_number = %s
        """
        stats = self.db.fetch_one(query, (account_number,))
        
        if stats:
            user.update({
                'total_transactions': stats['total_transactions'],
                'total_deposits': float(stats['total_deposits'] or 0),
                'total_withdrawals': float(stats['total_withdrawals'] or 0),
                'total_transfers_out': float(stats['total_transfers_out'] or 0),
                'total_transfers_in': float(stats['total_transfers_in'] or 0)
            })
        
        return user