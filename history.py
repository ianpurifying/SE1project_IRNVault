from database import Database
from datetime import datetime

class History:
    def __init__(self, db: Database):
        self.db = db

    def mini_statement(self, account_number: str, limit: int = 5):
        """Get mini statement data for console display"""
        self.db.connect()
        query = "SELECT timestamp, type, amount FROM transactions WHERE account_number = %s ORDER BY timestamp DESC LIMIT %s"
        self.db.cursor.execute(query, (account_number, limit))
        rows = self.db.cursor.fetchall()
        self.db.close()
        print("Mini Statement:")
        for ts, ttype, amt in rows:
            print(f"{ts}: {ttype} {amt}")

    def get_mini_statement_data(self, account_number: str, limit: int = 5):
        """Get mini statement data for GUI display"""
        try:
            self.db.connect()
            query = """SELECT timestamp, type, amount 
                      FROM transactions 
                      WHERE account_number = %s 
                      ORDER BY timestamp DESC 
                      LIMIT %s"""
            self.db.cursor.execute(query, (account_number, limit))
            rows = self.db.cursor.fetchall()
            self.db.close()
            return rows
        except Exception as e:
            self.db.close()
            return []

    def get_account_balance(self, account_number: str):
        """Calculate current account balance from transactions"""
        try:
            self.db.connect()
            query = """SELECT type, amount 
                      FROM transactions 
                      WHERE account_number = %s 
                      ORDER BY timestamp ASC"""
            self.db.cursor.execute(query, (account_number,))
            transactions = self.db.cursor.fetchall()
            self.db.close()
            
            balance = 0.00
            for trans_type, amount in transactions:
                if trans_type in ['deposit', 'transfer_in', 'loan_disbursement']:
                    balance += float(amount)
                elif trans_type in ['withdrawal', 'transfer_out', 'loan_payment']:
                    balance -= float(amount)
            
            return balance
        except Exception as e:
            self.db.close()
            return 0.00

    def format_mini_statement_text(self, account_number: str, limit: int = 5):
        """Format mini statement as text for GUI display"""
        try:
            transactions = self.get_mini_statement_data(account_number, limit)
            current_balance = self.get_account_balance(account_number)
            
            # Header
            statement_text = "=" * 60 + "\n"
            statement_text += "                    MINI STATEMENT\n"
            statement_text += "=" * 60 + "\n\n"
            
            statement_text += f"Account Number: {account_number}\n"
            statement_text += f"Statement Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            statement_text += f"Current Balance: ${current_balance:.2f}\n\n"
            
            statement_text += "Recent Transactions:\n"
            statement_text += "-" * 60 + "\n"
            statement_text += f"{'Date/Time':<20} {'Type':<18} {'Amount':<12}\n"
            statement_text += "-" * 60 + "\n"
            
            if transactions:
                # Calculate running balance for display (going backwards from current)
                running_balance = current_balance
                transaction_list = []
                
                for timestamp, trans_type, amount in transactions:
                    # Format timestamp
                    if isinstance(timestamp, str):
                        display_time = timestamp[:16]  # Show YYYY-MM-DD HH:MM
                    else:
                        display_time = timestamp.strftime('%Y-%m-%d %H:%M')
                    
                    # Format transaction type for better display
                    type_display = {
                        'deposit': 'Deposit',
                        'withdrawal': 'Withdrawal', 
                        'transfer_in': 'Transfer In',
                        'transfer_out': 'Transfer Out',
                        'loan_disbursement': 'Loan Disbursed',
                        'loan_payment': 'Loan Payment'
                    }.get(trans_type, trans_type.title())
                    
                    # Format amount with + or - sign
                    if trans_type in ['deposit', 'transfer_in', 'loan_disbursement']:
                        amount_str = f"+${float(amount):.2f}"
                    else:
                        amount_str = f"-${float(amount):.2f}"
                    
                    transaction_list.append(f"{display_time:<20} {type_display:<18} {amount_str:<12}")
                
                # Add all transactions to statement
                for transaction_line in transaction_list:
                    statement_text += transaction_line + "\n"
                    
            else:
                statement_text += "No transactions found for this account.\n"
            
            statement_text += "\n" + "-" * 60 + "\n"
            statement_text += f"{'Current Balance:':<40} ${current_balance:.2f}\n"
            statement_text += "=" * 60 + "\n"
            statement_text += "Thank you for banking with us!\n"
            statement_text += "=" * 60 + "\n"
            
            return statement_text
            
        except Exception as e:
            return f"Error generating statement: {str(e)}\n\nDebug info:\nAccount: {account_number}\nLimit: {limit}"