# banking_app/transactions/transaction_service.py
"""
Transaction service
Handles all banking transactions (deposit, withdrawal, transfer)
"""

from typing import Dict, Any, List
from decimal import Decimal
from db.database import Database

class TransactionService:
    def __init__(self, database: Database):
        self.db = database

    def deposit(self, account_number: str, amount: float) -> bool:
        """Process deposit transaction"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        try:
            self.db.begin_transaction()
            
            # Update account balance
            query = """
                UPDATE accounts 
                SET balance = balance + %s 
                WHERE account_number = %s
            """
            if not self.db.execute_query(query, (amount, account_number)):
                raise Exception("Failed to update balance")
            
            # Record transaction
            query = """
                INSERT INTO transactions (account_number, type, amount) 
                VALUES (%s, %s, %s)
            """
            if not self.db.execute_query(query, (account_number, 'deposit', amount)):
                raise Exception("Failed to record transaction")
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            raise Exception(f"Deposit failed: {str(e)}")

    def withdraw(self, account_number: str, amount: float) -> bool:
        """Process withdrawal transaction"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        try:
            self.db.begin_transaction()
            
            # Check current balance
            query = "SELECT balance FROM accounts WHERE account_number = %s"
            result = self.db.fetch_one(query, (account_number,))
            
            if not result:
                raise Exception("Account not found")
            
            current_balance = float(result['balance'])
            if current_balance < amount:
                raise Exception("Insufficient balance")
            
            # Update account balance
            query = """
                UPDATE accounts 
                SET balance = balance - %s 
                WHERE account_number = %s
            """
            if not self.db.execute_query(query, (amount, account_number)):
                raise Exception("Failed to update balance")
            
            # Record transaction
            query = """
                INSERT INTO transactions (account_number, type, amount) 
                VALUES (%s, %s, %s)
            """
            if not self.db.execute_query(query, (account_number, 'withdrawal', amount)):
                raise Exception("Failed to record transaction")
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            raise Exception(f"Withdrawal failed: {str(e)}")

    def transfer(self, from_account: str, to_account: str, amount: float) -> bool:
        """Process transfer transaction"""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        
        if from_account == to_account:
            raise ValueError("Cannot transfer to the same account")
        
        try:
            self.db.begin_transaction()
            
            # Check sender balance
            query = "SELECT balance FROM accounts WHERE account_number = %s"
            result = self.db.fetch_one(query, (from_account,))
            
            if not result:
                raise Exception("Sender account not found")
            
            sender_balance = float(result['balance'])
            if sender_balance < amount:
                raise Exception("Insufficient balance")
            
            # Check recipient exists
            query = "SELECT account_number FROM accounts WHERE account_number = %s"
            if not self.db.fetch_one(query, (to_account,)):
                raise Exception("Recipient account not found")
            
            # Update sender balance
            query = """
                UPDATE accounts 
                SET balance = balance - %s 
                WHERE account_number = %s
            """
            if not self.db.execute_query(query, (amount, from_account)):
                raise Exception("Failed to update sender balance")
            
            # Update recipient balance
            query = """
                UPDATE accounts 
                SET balance = balance + %s 
                WHERE account_number = %s
            """
            if not self.db.execute_query(query, (amount, to_account)):
                raise Exception("Failed to update recipient balance")
            
            # Record sender transaction
            query = """
                INSERT INTO transactions (account_number, type, amount) 
                VALUES (%s, %s, %s)
            """
            if not self.db.execute_query(query, (from_account, 'transfer_out', amount)):
                raise Exception("Failed to record sender transaction")
            
            # Record recipient transaction
            if not self.db.execute_query(query, (to_account, 'transfer_in', amount)):
                raise Exception("Failed to record recipient transaction")
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            raise Exception(f"Transfer failed: {str(e)}")

    def get_transaction_history(self, account_number: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get transaction history for account"""
        query = """
            SELECT type, amount, timestamp 
            FROM transactions 
            WHERE account_number = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
        """
        results = self.db.fetch_all(query, (account_number, limit))
        
        return [{
            'type': row['type'],
            'amount': float(row['amount']),
            'timestamp': row['timestamp']
        } for row in results]