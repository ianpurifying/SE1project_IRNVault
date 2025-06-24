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

    def reject_account(self, account_number: str, reason: str) -> bool:
        """Reject a pending account and record reason with full account data"""
        try:
            self.db.begin_transaction()
            
            # Get full account info before deletion
            check_query = """
                SELECT name, hashed_pin, balance 
                FROM accounts 
                WHERE account_number = %s AND is_approved = 0
            """
            account_info = self.db.fetch_one(check_query, (account_number,))
            
            if not account_info:
                self.db.rollback_transaction()
                return False
            
            # Record rejection with full account data (if schema is enhanced)
            decline_query = """
                INSERT INTO account_declines (account_number, name, hashed_pin, original_balance, reason) 
                VALUES (%s, %s, %s, %s, %s)
            """
            if not self.db.execute_query(decline_query, (
                account_number, 
                account_info['name'], 
                account_info['hashed_pin'],
                account_info['balance'],
                reason
            )):
                raise Exception("Failed to record rejection reason")
            
            # Delete the account
            delete_query = "DELETE FROM accounts WHERE account_number = %s AND is_approved = 0"
            if not self.db.execute_query(delete_query, (account_number,)):
                raise Exception("Failed to delete account")
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            return False

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

    def update_user_details(self, account_number: str, name: str = None, balance: float = None) -> bool:
        """Update user details (name and/or balance)"""
        if account_number == '0000000001':
            return False  # Cannot update admin account
        
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            
            if balance is not None:
                updates.append("balance = %s")
                params.append(balance)
            
            if not updates:
                return False  # Nothing to update
            
            query = f"""
                UPDATE accounts 
                SET {', '.join(updates)} 
                WHERE account_number = %s AND account_number != '0000000001'
            """
            params.append(account_number)
            
            return self.db.execute_query(query, tuple(params))
            
        except Exception as e:
            return False

    def delete_user_account(self, account_number: str) -> bool:
        """Delete a user account and all related data (enhanced version of existing delete_account)"""
        if account_number == '0000000001':
            return False  # Cannot delete admin account
        
        try:
            self.db.begin_transaction()
            
            # Delete loan payments first (due to foreign key constraints)
            query = "DELETE FROM loan_payments WHERE account_number = %s"
            self.db.execute_query(query, (account_number,))
            
            # Delete loans
            query = "DELETE FROM loans WHERE account_number = %s"
            self.db.execute_query(query, (account_number,))
            
            # Delete loan applications
            query = "DELETE FROM loan_applications WHERE account_number = %s"
            self.db.execute_query(query, (account_number,))
            
            # Delete transactions
            query = "DELETE FROM transactions WHERE account_number = %s"
            self.db.execute_query(query, (account_number,))
            
            # Delete account declines (if any)
            query = "DELETE FROM account_declines WHERE account_number = %s"
            self.db.execute_query(query, (account_number,))
            
            # Delete the account itself
            query = "DELETE FROM accounts WHERE account_number = %s"
            if not self.db.execute_query(query, (account_number,)):
                raise Exception("Failed to delete account")
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            return False

    def toggle_user_status(self, account_number: str) -> bool:
        """Toggle user approval status (approved <-> suspended)"""
        if account_number == '0000000001':
            return False  # Cannot modify admin account
        
        try:
            # Get current status
            query = "SELECT is_approved FROM accounts WHERE account_number = %s"
            result = self.db.fetch_one(query, (account_number,))
            
            if not result:
                return False
            
            new_status = 0 if result['is_approved'] else 1
            
            query = """
                UPDATE accounts 
                SET is_approved = %s 
                WHERE account_number = %s AND account_number != '0000000001'
            """
            return self.db.execute_query(query, (new_status, account_number))
            
        except Exception as e:
            return False

    def get_user_transaction_summary(self, account_number: str) -> Dict[str, Any]:
        """Get user's transaction summary with counts by period"""
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        month_start = today.replace(day=1)
        year_start = today.replace(month=1, day=1)
        
        # Get transaction counts by period
        query = """
            SELECT 
                COUNT(CASE WHEN DATE(timestamp) = %s THEN 1 END) as today_count,
                COUNT(CASE WHEN DATE(timestamp) >= %s THEN 1 END) as month_count,
                COUNT(CASE WHEN DATE(timestamp) >= %s THEN 1 END) as year_count,
                COUNT(*) as total_count
            FROM transactions 
            WHERE account_number = %s
        """
        result = self.db.fetch_one(query, (today, month_start, year_start, account_number))
        
        return {
            'today': result['today_count'] if result else 0,
            'this_month': result['month_count'] if result else 0,
            'this_year': result['year_count'] if result else 0,
            'total': result['total_count'] if result else 0
        }

    def get_user_transactions_by_period(self, account_number: str, period: str) -> List[Dict[str, Any]]:
        """Get user transactions filtered by period (today/month/year/all)"""
        from datetime import datetime
        
        today = datetime.now().date()
        
        # Define period filters
        period_filters = {
            'today': f"DATE(timestamp) = '{today}'",
            'month': f"DATE(timestamp) >= '{today.replace(day=1)}'",
            'year': f"DATE(timestamp) >= '{today.replace(month=1, day=1)}'",
            'all': "1=1"  # No filter
        }
        
        where_clause = period_filters.get(period, period_filters['all'])
        
        query = f"""
            SELECT id, type, amount, timestamp
            FROM transactions 
            WHERE account_number = %s AND {where_clause}
            ORDER BY timestamp DESC
            LIMIT 100
        """
        
        results = self.db.fetch_all(query, (account_number,))
        
        return [{
            'id': row['id'],
            'type': row['type'],
            'amount': float(row['amount']),
            'timestamp': row['timestamp'],
            'formatted_amount': f"₱{float(row['amount']):,.2f}",
            'type_display': self._format_transaction_type(row['type'])
        } for row in results]

    def _format_transaction_type(self, transaction_type: str) -> str:
        """Format transaction type for display"""
        type_map = {
            'deposit': '💰 Deposit',
            'withdrawal': '💸 Withdrawal', 
            'transfer_in': '📥 Transfer In',
            'transfer_out': '📤 Transfer Out',
            'loan_disbursement': '🏦 Loan Disbursement',
            'loan_payment': '💳 Loan Payment'
        }
        return type_map.get(transaction_type, transaction_type.title())

    def get_declined_accounts(self) -> List[Dict[str, Any]]:
        """Get all declined/suspended accounts from account_declines table"""
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

    def reactivate_declined_account(self, account_number: str) -> bool:
        """Reactivate a declined account by moving it back to accounts table"""
        try:
            self.db.begin_transaction()
            
            # Get full declined account info (enhanced schema)
            check_query = """
                SELECT account_number, name, hashed_pin, original_balance, reason 
                FROM account_declines 
                WHERE account_number = %s
            """
            declined_record = self.db.fetch_one(check_query, (account_number,))
            
            if not declined_record:
                self.db.rollback_transaction()
                return False
            
            # Restore account with original data and approved status
            insert_query = """
                INSERT INTO accounts (account_number, name, hashed_pin, balance, is_approved) 
                VALUES (%s, %s, %s, %s, 1)
            """
            if not self.db.execute_query(insert_query, (
                declined_record['account_number'],
                declined_record['name'],
                declined_record['hashed_pin'],
                declined_record['original_balance']
            )):
                raise Exception("Failed to reactivate account")
            
            # Remove from declines table
            delete_query = "DELETE FROM account_declines WHERE account_number = %s"
            if not self.db.execute_query(delete_query, (account_number,)):
                raise Exception("Failed to remove from declines table")
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            return False

    def delete_declined_account_permanently(self, account_number: str) -> bool:
        """Permanently delete a declined account from account_declines table"""
        query = "DELETE FROM account_declines WHERE account_number = %s"
        return self.db.execute_query(query, (account_number,))