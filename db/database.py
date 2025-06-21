# banking_app/db/database.py
import mysql.connector
from mysql.connector import Error
import os
from typing import Dict, List, Optional, Any

class Database:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'se1project'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'port': int(os.getenv('DB_PORT', 3306)),
            'charset': 'utf8mb4',
            'autocommit': True
        }
        self.connection = None

    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query: str, params: tuple = None) -> bool:
        """Execute a query that doesn't return results (INSERT, UPDATE, DELETE)"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Query execution error: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """Fetch a single row from the database"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Fetch error: {e}")
            return None

    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Fetch all rows from the database"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Fetch all error: {e}")
            return []

    def begin_transaction(self):
        """Start a database transaction"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            self.connection.start_transaction()
        except Error as e:
            print(f"Transaction start error: {e}")
            raise

    def commit_transaction(self):
        """Commit the current transaction"""
        try:
            self.connection.commit()
        except Error as e:
            print(f"Transaction commit error: {e}")
            raise

    def rollback_transaction(self):
        """Rollback the current transaction"""
        try:
            self.connection.rollback()
        except Error as e:
            print(f"Transaction rollback error: {e}")
            raise

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()