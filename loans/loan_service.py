from typing import Optional, Dict, Any, List
from decimal import Decimal
from datetime import datetime, timedelta
from db.database import Database

class LoanService:
    def __init__(self, database: Database):
        self.db = database

    def apply_for_loan(self, account_number: str, amount: float, purpose: str, 
                      monthly_income: float, employment_status: str) -> int:
        """Submit a new loan application"""
        query = """
            INSERT INTO loan_applications 
            (account_number, amount, purpose, monthly_income, employment_status)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        if not self.db.execute_query(query, (account_number, amount, purpose, 
                                           monthly_income, employment_status)):
            raise Exception("Failed to submit loan application")
        
        # Get the application ID
        result = self.db.fetch_one("SELECT LAST_INSERT_ID() as id")
        return result['id'] if result else None

    def get_loan_applications(self, account_number: str) -> List[Dict[str, Any]]:
        """Get all loan applications for an account"""
        query = """
            SELECT id, amount, purpose, monthly_income, employment_status, 
                   status, interest_rate, term_months, monthly_payment,
                   admin_notes, applied_at, processed_at
            FROM loan_applications 
            WHERE account_number = %s 
            ORDER BY applied_at DESC
        """
        
        results = self.db.fetch_all(query, (account_number,))
        return [{
            'id': row['id'],
            'amount': float(row['amount']),
            'purpose': row['purpose'],
            'monthly_income': float(row['monthly_income']),
            'employment_status': row['employment_status'],
            'status': row['status'],
            'interest_rate': float(row['interest_rate']) if row['interest_rate'] else None,
            'term_months': row['term_months'],
            'monthly_payment': float(row['monthly_payment']) if row['monthly_payment'] else None,
            'admin_notes': row['admin_notes'],
            'applied_at': row['applied_at'],
            'processed_at': row['processed_at']
        } for row in results]

    def get_active_loans(self, account_number: str) -> List[Dict[str, Any]]:
        """Get all active loans for an account"""
        query = """
            SELECT l.id, l.application_id, l.principal_amount, l.interest_rate,
                   l.term_months, l.monthly_payment, l.remaining_balance,
                   l.next_payment_date, l.status, l.disbursed_at,
                   la.purpose
            FROM loans l
            JOIN loan_applications la ON l.application_id = la.id
            WHERE l.account_number = %s AND l.status = 'active'
            ORDER BY l.disbursed_at DESC
        """
        
        results = self.db.fetch_all(query, (account_number,))
        return [{
            'id': row['id'],
            'application_id': row['application_id'],
            'principal_amount': float(row['principal_amount']),
            'interest_rate': float(row['interest_rate']),
            'term_months': row['term_months'],
            'monthly_payment': float(row['monthly_payment']),
            'remaining_balance': float(row['remaining_balance']),
            'next_payment_date': row['next_payment_date'],
            'status': row['status'],
            'disbursed_at': row['disbursed_at'],
            'purpose': row['purpose']
        } for row in results]

    def make_loan_payment(self, loan_id: int, account_number: str, 
                        payment_amount: float, payment_type: str = 'regular') -> bool:
        """Process a loan payment - FIXED VERSION"""
        try:
            # Get loan details
            loan_query = """
                SELECT remaining_balance, interest_rate, monthly_payment, next_payment_date
                FROM loans 
                WHERE id = %s AND account_number = %s AND status = 'active'
            """
            loan = self.db.fetch_one(loan_query, (loan_id, account_number))
            
            if not loan:
                raise Exception("Loan not found or not active")
            
            # Check if account has sufficient balance
            account_query = "SELECT balance FROM accounts WHERE account_number = %s"
            account = self.db.fetch_one(account_query, (account_number,))
            
            if not account:
                raise Exception("Account not found")
            
            current_balance = float(account['balance'])
            if current_balance < payment_amount:
                raise Exception("Insufficient funds for loan payment")
            
            remaining_balance = float(loan['remaining_balance'])
            interest_rate = float(loan['interest_rate'])
            
            # FIXED: Calculate interest portion based on remaining balance
            # Monthly interest rate calculation
            monthly_interest_rate = interest_rate / 100 / 12
            interest_portion = remaining_balance * monthly_interest_rate
            
            # Principal portion is what's left after interest
            principal_portion = payment_amount - interest_portion
            
            # Ensure principal portion is not negative (shouldn't happen with proper payments)
            if principal_portion < 0:
                principal_portion = 0
                interest_portion = payment_amount
            
            # Calculate new remaining balance
            new_loan_balance = max(0, remaining_balance - principal_portion)
            
            # CRITICAL FIX: Update account balance FIRST, then record everything else
            new_account_balance = current_balance - payment_amount
            update_account_query = """
                UPDATE accounts 
                SET balance = %s 
                WHERE account_number = %s
            """
            
            if not self.db.execute_query(update_account_query, (new_account_balance, account_number)):
                raise Exception("Failed to update account balance")
            
            # Record the payment in loan_payments table
            payment_query = """
                INSERT INTO loan_payments 
                (loan_id, account_number, payment_amount, principal_portion, 
                interest_portion, remaining_balance, payment_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            if not self.db.execute_query(payment_query, (
                loan_id, account_number, payment_amount, principal_portion,
                interest_portion, new_loan_balance, payment_type
            )):
                raise Exception("Failed to record payment")
            
            # Update loan table with new balance and next payment date
            next_payment_date = loan['next_payment_date']
            if isinstance(next_payment_date, str):
                next_payment_date = datetime.strptime(next_payment_date, '%Y-%m-%d').date()
            
            new_next_payment = next_payment_date + timedelta(days=30)
            loan_status = 'paid_off' if new_loan_balance == 0 else 'active'
            
            update_loan_query = """
                UPDATE loans 
                SET remaining_balance = %s, next_payment_date = %s, status = %s
                WHERE id = %s
            """
            
            if not self.db.execute_query(update_loan_query, (
                new_loan_balance, new_next_payment, loan_status, loan_id
            )):
                raise Exception("Failed to update loan")
            
            # Record transaction
            transaction_query = """
                INSERT INTO transactions (account_number, type, amount)
                VALUES (%s, 'loan_payment', %s)
            """
            
            self.db.execute_query(transaction_query, (account_number, payment_amount))
            
            return True
            
        except Exception as e:
            raise Exception(f"Payment processing failed: {str(e)}")

    def get_loan_payment_history(self, account_number: str, loan_id: int = None) -> List[Dict[str, Any]]:
        """Get payment history for loans"""
        if loan_id:
            query = """
                SELECT lp.*, l.principal_amount
                FROM loan_payments lp
                JOIN loans l ON lp.loan_id = l.id
                WHERE lp.account_number = %s AND lp.loan_id = %s
                ORDER BY lp.payment_date DESC
            """
            params = (account_number, loan_id)
        else:
            query = """
                SELECT lp.*, l.principal_amount
                FROM loan_payments lp
                JOIN loans l ON lp.loan_id = l.id
                WHERE lp.account_number = %s
                ORDER BY lp.payment_date DESC
            """
            params = (account_number,)
        
        results = self.db.fetch_all(query, params)
        return [{
            'id': row['id'],
            'loan_id': row['loan_id'],
            'payment_amount': float(row['payment_amount']),
            'principal_portion': float(row['principal_portion']),
            'interest_portion': float(row['interest_portion']),
            'remaining_balance': float(row['remaining_balance']),
            'payment_date': row['payment_date'],
            'payment_type': row['payment_type']
        } for row in results]

    def calculate_monthly_payment(self, principal: float, annual_rate: float, months: int) -> float:
        """Calculate monthly payment using loan formula"""
        if annual_rate == 0:
            return principal / months
        
        monthly_rate = annual_rate / 100 / 12
        payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
                 ((1 + monthly_rate) ** months - 1)
        return round(payment, 2)

    def validate_account_loan_sync(self, account_number: str) -> Dict[str, Any]:
        """
        Validate that account balance and loan data are properly synchronized
        """
        # Get current account balance
        account_query = "SELECT balance FROM accounts WHERE account_number = %s"
        account = self.db.fetch_one(account_query, (account_number,))
        current_account_balance = float(account['balance']) if account else 0
        
        # Get all loan disbursements (money added to account)
        disbursement_query = """
            SELECT COALESCE(SUM(amount), 0) as total_disbursed
            FROM transactions 
            WHERE account_number = %s AND type = 'loan_disbursement'
        """
        disbursement = self.db.fetch_one(disbursement_query, (account_number,))
        total_disbursed = float(disbursement['total_disbursed']) if disbursement else 0
        
        # Get all loan payments made (money deducted from account)
        payment_query = """
            SELECT COALESCE(SUM(amount), 0) as total_payments
            FROM transactions 
            WHERE account_number = %s AND type = 'loan_payment'
        """
        payment = self.db.fetch_one(payment_query, (account_number,))
        total_payments = float(payment['total_payments']) if payment else 0
        
        # Get other transactions to calculate what account balance should be
        other_transactions_query = """
            SELECT COALESCE(SUM(CASE 
                WHEN type IN ('deposit', 'transfer_in', 'loan_disbursement') THEN amount
                WHEN type IN ('withdrawal', 'transfer_out', 'loan_payment') THEN -amount
                ELSE 0 
            END), 0) as net_transactions
            FROM transactions 
            WHERE account_number = %s
        """
        other_transactions = self.db.fetch_one(other_transactions_query, (account_number,))
        expected_balance_from_transactions = float(other_transactions['net_transactions']) if other_transactions else 0
        
        # Get current loan balances
        loan_balance_query = """
            SELECT COALESCE(SUM(remaining_balance), 0) as total_loan_balance
            FROM loans 
            WHERE account_number = %s AND status = 'active'
        """
        loan_balance = self.db.fetch_one(loan_balance_query, (account_number,))
        total_loan_balance = float(loan_balance['total_loan_balance']) if loan_balance else 0
        
        return {
            'account_number': account_number,
            'current_account_balance': current_account_balance,
            'expected_balance_from_transactions': expected_balance_from_transactions,
            'balance_matches': abs(current_account_balance - expected_balance_from_transactions) < 0.01,
            'total_loan_disbursements': total_disbursed,
            'total_loan_payments': total_payments,
            'remaining_loan_balance': total_loan_balance,
            'net_cash_position': current_account_balance - total_loan_balance
        }

    def repair_account_balance(self, account_number: str) -> bool:
        """
        Repair account balance based on transaction history
        Use this if you suspect the account balance is incorrect
        """
        try:
            # Calculate correct balance from all transactions
            transaction_query = """
                SELECT COALESCE(SUM(CASE 
                    WHEN type IN ('deposit', 'transfer_in', 'loan_disbursement') THEN amount
                    WHEN type IN ('withdrawal', 'transfer_out', 'loan_payment') THEN -amount
                    ELSE 0 
                END), 0) as correct_balance
                FROM transactions 
                WHERE account_number = %s
            """
            
            result = self.db.fetch_one(transaction_query, (account_number,))
            correct_balance = float(result['correct_balance']) if result else 0
            
            # Update account balance
            update_query = """
                UPDATE accounts 
                SET balance = %s 
                WHERE account_number = %s
            """
            
            return self.db.execute_query(update_query, (correct_balance, account_number))
            
        except Exception as e:
            raise Exception(f"Failed to repair account balance: {str(e)}")