# banking_app/statements/statement_service.py
"""
Statement service
Handles mini statements and transaction filtering
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from db.database import Database

class StatementService:
    def __init__(self, database: Database):
        self.db = database

    def get_daily_statement(self, account_number: str) -> List[Dict[str, Any]]:
        """Get today's transactions"""
        query = """
            SELECT type, amount, timestamp 
            FROM transactions 
            WHERE account_number = %s 
            AND DATE(timestamp) = CURDATE()
            ORDER BY timestamp DESC
        """
        results = self.db.fetch_all(query, (account_number,))
        
        return [{
            'type': row['type'],
            'amount': float(row['amount']),
            'timestamp': row['timestamp']
        } for row in results]

    def get_monthly_statement(self, account_number: str) -> List[Dict[str, Any]]:
        """Get this month's transactions"""
        query = """
            SELECT type, amount, timestamp 
            FROM transactions 
            WHERE account_number = %s 
            AND YEAR(timestamp) = YEAR(CURDATE()) 
            AND MONTH(timestamp) = MONTH(CURDATE())
            ORDER BY timestamp DESC
        """
        results = self.db.fetch_all(query, (account_number,))
        
        return [{
            'type': row['type'],
            'amount': float(row['amount']),
            'timestamp': row['timestamp']
        } for row in results]

    def get_yearly_statement(self, account_number: str) -> List[Dict[str, Any]]:
        """Get this year's transactions"""
        query = """
            SELECT type, amount, timestamp 
            FROM transactions 
            WHERE account_number = %s 
            AND YEAR(timestamp) = YEAR(CURDATE())
            ORDER BY timestamp DESC
        """
        results = self.db.fetch_all(query, (account_number,))
        
        return [{
            'type': row['type'],
            'amount': float(row['amount']),
            'timestamp': row['timestamp']
        } for row in results]

    def get_all_transactions(self, account_number: str) -> List[Dict[str, Any]]:
        """Get all transactions for account"""
        query = """
            SELECT type, amount, timestamp 
            FROM transactions 
            WHERE account_number = %s 
            ORDER BY timestamp DESC
        """
        results = self.db.fetch_all(query, (account_number,))
        
        return [{
            'type': row['type'],
            'amount': float(row['amount']),
            'timestamp': row['timestamp']
        } for row in results]

    def get_statement_by_date_range(self, account_number: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get transactions within date range"""
        query = """
            SELECT type, amount, timestamp 
            FROM transactions 
            WHERE account_number = %s 
            AND DATE(timestamp) BETWEEN %s AND %s
            ORDER BY timestamp DESC
        """
        results = self.db.fetch_all(query, (account_number, start_date, end_date))
        
        return [{
            'type': row['type'],
            'amount': float(row['amount']),
            'timestamp': row['timestamp']
        } for row in results]

    def get_statement_summary(self, account_number: str, period: str = 'monthly') -> Dict[str, Any]:
        """Get transaction summary for specified period"""
        if period == 'daily':
            transactions = self.get_daily_statement(account_number)
        elif period == 'monthly':
            transactions = self.get_monthly_statement(account_number)
        elif period == 'yearly':
            transactions = self.get_yearly_statement(account_number)
        else:
            transactions = self.get_all_transactions(account_number)
        
        # Calculate summary
        total_deposits = sum(t['amount'] for t in transactions if t['type'] == 'deposit')
        total_withdrawals = sum(t['amount'] for t in transactions if t['type'] == 'withdrawal')
        total_transfers_in = sum(t['amount'] for t in transactions if t['type'] == 'transfer_in')
        total_transfers_out = sum(t['amount'] for t in transactions if t['type'] == 'transfer_out')
        
        return {
            'period': period,
            'total_transactions': len(transactions),
            'total_deposits': total_deposits,
            'total_withdrawals': total_withdrawals,
            'total_transfers_in': total_transfers_in,
            'total_transfers_out': total_transfers_out,
            'net_amount': total_deposits + total_transfers_in - total_withdrawals - total_transfers_out
        }

    def export_statement(self, account_number: str, period: str = 'monthly') -> str:
        """Export statement as formatted string"""
        if period == 'daily':
            transactions = self.get_daily_statement(account_number)
            title = "Daily Statement"
        elif period == 'monthly':
            transactions = self.get_monthly_statement(account_number)
            title = "Monthly Statement"
        elif period == 'yearly':
            transactions = self.get_yearly_statement(account_number)
            title = "Yearly Statement"
        else:
            transactions = self.get_all_transactions(account_number)
            title = "Complete Statement"
        
        # Format statement
        statement = f"\n{'='*50}\n"
        statement += f"      {title}\n"
        statement += f"      Account: {account_number}\n"
        statement += f"      Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        statement += f"{'='*50}\n\n"
        
        if not transactions:
            statement += "No transactions found for this period.\n"
        else:
            statement += f"{'Type':<15} {'Amount':<12} {'Date':<20}\n"
            statement += f"{'-'*47}\n"
            
            for txn in transactions:
                statement += f"{txn['type']:<15} ₱{txn['amount']:<11.2f} {txn['timestamp']}\n"
            
            # Add summary
            summary = self.get_statement_summary(account_number, period)
            statement += f"\n{'-'*47}\n"
            statement += f"Summary:\n"
            statement += f"Total Transactions: {summary['total_transactions']}\n"
            statement += f"Total Deposits: ₱{summary['total_deposits']:.2f}\n"
            statement += f"Total Withdrawals: ₱{summary['total_withdrawals']:.2f}\n"
            statement += f"Net Amount: ₱{summary['net_amount']:.2f}\n"
        
        return statement