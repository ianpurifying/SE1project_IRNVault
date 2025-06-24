# banking_app/auth/auth_service.py
"""
Authentication service
Handles user registration, login, and password management
"""

import bcrypt
import random
import string
from typing import Optional, Dict, Any
from db.database import Database

class AuthService:
    def __init__(self, database: Database):
        self.db = database

    def register_user(self, name: str, password: str) -> str:
        """Register a new user and return account number"""
        # Validate input
        if not name or not password:
            raise ValueError("Name and password are required")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        # Generate unique account number
        account_number = self._generate_account_number()
        
        # Hash password
        hashed_password = self._hash_password(password)
        
        # Insert user into database
        query = """
            INSERT INTO accounts (account_number, name, hashed_pin, balance, is_approved) 
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (account_number, name, hashed_password, 0.00, 0)
        
        if self.db.execute_query(query, params):
            return account_number
        else:
            raise Exception("Failed to create account")

    def login(self, account_number: str, password: str) -> Dict[str, Any]:
        """Authenticate user and return user data"""
        if not account_number or not password:
            raise ValueError("Account number and password are required")
        
        # First check if account was declined
        decline_query = """
            SELECT reason, declined_at 
            FROM account_declines 
            WHERE account_number = %s 
            ORDER BY declined_at DESC 
            LIMIT 1
        """
        decline_record = self.db.fetch_one(decline_query, (account_number,))
        
        if decline_record:
            # Account was declined, show the reason
            decline_reason = decline_record['reason']
            decline_date = decline_record['declined_at']
            raise ValueError(f"Account registration was declined. Reason: {decline_reason}")
        
        # Get user from database
        query = "SELECT * FROM accounts WHERE account_number = %s"
        user = self.db.fetch_one(query, (account_number,))
        
        if not user:
            raise ValueError("Invalid account number or password")
        
        # Verify password
        if not self._verify_password(password, user['hashed_pin']):
            raise ValueError("Invalid account number or password")
        
        # Check if account is approved (except for admin)
        if account_number != '0000000001' and not user['is_approved']:
            raise ValueError("Account is pending approval. Please wait for admin approval.")
        
        # Return user data (excluding password hash)
        return {
            'account_number': user['account_number'],
            'name': user['name'],
            'balance': float(user['balance']),
            'is_approved': user['is_approved'],
            'created_at': user['created_at']
        }

    def _generate_account_number(self) -> str:
        """Generate a unique 10-digit account number"""
        while True:
            # Generate random 10-digit number
            account_number = ''.join(random.choices(string.digits, k=10))
            
            # Ensure it doesn't start with 0 (except admin account)
            if account_number[0] == '0':
                continue
            
            # Check if account number already exists
            query = "SELECT account_number FROM accounts WHERE account_number = %s"
            if not self.db.fetch_one(query, (account_number,)):
                return account_number

    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def change_password(self, account_number: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        # Verify old password
        user = self.login(account_number, old_password)
        if not user:
            return False
        
        # Validate new password
        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters long")
        
        # Hash new password
        hashed_password = self._hash_password(new_password)
        
        # Update password in database
        query = "UPDATE accounts SET hashed_pin = %s WHERE account_number = %s"
        return self.db.execute_query(query, (hashed_password, account_number))