# banking_app/admin/admin_service.py
"""
Admin service
Handles admin operations like account approval and user management
"""

from typing import List, Dict, Any, Optional
from db.database import Database

class AdminService:
    def __init__(self, database: Database):
        self.db = database

    def get_pending_accounts(self) -> List[Dict[str, Any]]:
        """Get all pending accounts"""
        query = """
            SELECT account_number, name, created_at 
            FROM accounts 
            WHERE is_approved = 0 AND account_number != '0000000001'
            ORDER BY created_at ASC
        """
        results = self.db.fetch_all(query)
        
        return [{
            'account_number': row['account_number'],
            'name': row['name'],
            'created_at': row['created_at']
        } for row in results]

    def approve_account(self, account_number: str) -> bool:
        """Approve a pending account"""
        query = """
            UPDATE accounts 
            SET is_approved = 1 
            WHERE account_number = %s AND is_approved = 0
        """
        return self.db.execute_query(query, (account_number,))

    def reject_account(self, account_number: str, reason: str) -> bool:
        """Reject a pending account and record reason"""
        try:
            self.db.begin_transaction()
            
            # Record rejection reason
            query = """
                INSERT INTO account_declines (account_number, reason) 
                VALUES (%s, %s)
            """
            if not self.db.execute_query(query, (account_number, reason)):
                raise Exception("Failed to record rejection reason")
            
            # Delete the account
            query = "DELETE FROM accounts WHERE account_number = %s AND is_approved = 0"
            if not self.db.execute_query(query, (account_number,)):
                raise Exception("Failed to delete account")
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            return False

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (excluding admin)"""
        query = """
            SELECT account_number, name, balance, is_approved, created_at 
            FROM accounts 
            WHERE account_number != '0000000001'
            ORDER BY created_at DESC
        """
        results = self.db.fetch_all(query)
        
        return [{
            'account_number': row['account_number'],
            'name': row['name'],
            'balance': float(row['balance']),
            'is_approved': row['is_approved'],
            'created_at': row['created_at']
        } for row in results]

    def get_user_details(self, account_number: str) -> Optional[Dict[str, Any]]:
        """Get detailed user information"""
        query = """
            SELECT account_number, name, balance, is_approved, created_at 
            FROM accounts 
            WHERE account_number = %s
        """
        user = self.db.fetch_one(query, (account_number,))
        
        if not user:
            return None
        
        # Get transaction count
        query = "SELECT COUNT(*) as transaction_count FROM transactions WHERE account_number = %s"
        result = self.db.fetch_one(query, (account_number,))
        transaction_count = result['transaction_count'] if result else 0
        
        return {
            'account_number': user['account_number'],
            'name': user['name'],
            'balance': float(user['balance']),
            'is_approved': user['is_approved'],
            'created_at': user['created_at'],
            'transaction_count': transaction_count
        }

    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system-wide statistics"""
        stats = {}
        
        # Total users
        query = "SELECT COUNT(*) as total FROM accounts WHERE account_number != '0000000001'"
        result = self.db.fetch_one(query)
        stats['total_users'] = result['total'] if result else 0
        
        # Approved users
        query = "SELECT COUNT(*) as approved FROM accounts WHERE is_approved = 1 AND account_number != '0000000001'"
        result = self.db.fetch_one(query)
        stats['approved_users'] = result['approved'] if result else 0
        
        # Pending users
        query = "SELECT COUNT(*) as pending FROM accounts WHERE is_approved = 0"
        result = self.db.fetch_one(query)
        stats['pending_users'] = result['pending'] if result else 0
        
        # Total transactions
        query = "SELECT COUNT(*) as total FROM transactions"
        result = self.db.fetch_one(query)
        stats['total_transactions'] = result['total'] if result else 0
        
        # Total system balance
        query = "SELECT SUM(balance) as total_balance FROM accounts WHERE account_number != '0000000001'"
        result = self.db.fetch_one(query)
        stats['total_balance'] = float(result['total_balance']) if result and result['total_balance'] else 0.0
        
        return stats

    def get_rejected_accounts(self) -> List[Dict[str, Any]]:
        """Get list of rejected accounts with reasons"""
        query = """
            SELECT account_number, reason, declined_at 
            FROM account_declines 
            ORDER BY declined_at DESC
        """
        results = self.db.fetch_all(query)
        
        return [{
            'account_number': row['account_number'],
            'reason': row['reason'],
            'declined_at': row['declined_at']
        } for row in results]

    def suspend_account(self, account_number: str) -> bool:
        """Suspend an account (set approval to 0)"""
        query = """
            UPDATE accounts 
            SET is_approved = 0 
            WHERE account_number = %s AND account_number != '0000000001'
        """
        return self.db.execute_query(query, (account_number,))

    def reactivate_account(self, account_number: str) -> bool:
        """Reactivate a suspended account"""
        query = """
            UPDATE accounts 
            SET is_approved = 1 
            WHERE account_number = %s AND account_number != '0000000001'
        """
        return self.db.execute_query(query, (account_number,))

    def delete_account(self, account_number: str) -> bool:
        """Delete an account and all its transactions"""
        if account_number == '0000000001':
            return False  # Cannot delete admin account
        
        try:
            self.db.begin_transaction()
            
            # Delete transactions first
            query = "DELETE FROM transactions WHERE account_number = %s"
            self.db.execute_query(query, (account_number,))
            
            # Delete account
            query = "DELETE FROM accounts WHERE account_number = %s"
            if not self.db.execute_query(query, (account_number,)):
                raise Exception("Failed to delete account")
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            return False
