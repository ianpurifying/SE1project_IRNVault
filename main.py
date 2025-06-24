# banking_app/main.py
"""
Main entry point for the Banking System
Now uses GUI interface instead of command-line interface
"""

from auth.auth_service import AuthService
from users.user_service import UserService
from transactions.transaction_service import TransactionService
from statements.statement_service import StatementService
from admin.admin_service import AdminService
from loans.loan_service import LoanService
from db.database import Database
from gui.gui_manager import GUIManager
from typing import Dict, Any
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('banking_app.log'),
        logging.StreamHandler()
    ]
)

class BankingApp:
    def __init__(self):
        """Initialize the banking application with all services"""
        try:
            # Initialize database and services
            self.db = Database()
            self.auth_service = AuthService(self.db)
            self.user_service = UserService(self.db)
            self.transaction_service = TransactionService(self.db)
            self.statement_service = StatementService(self.db)
            self.admin_service = AdminService(self.db)
            self.loan_service = LoanService(self.db)
            
            # User session management
            self.current_user = None
            self.is_admin = False
            
            # Initialize GUI manager
            self.gui_manager = GUIManager(self)
            
            logging.info("Banking application initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize banking application: {str(e)}")
            raise

    def run(self):
        """Start the banking application with GUI"""
        try:
            logging.info("Starting banking application GUI")
            print("Starting IRN Vault Banking System...")
            self.gui_manager.start()
            
        except Exception as e:
            logging.error(f"Application error: {str(e)}")
            print(f"Application error: {str(e)}")
            sys.exit(1)

    def shutdown(self):
        """Safely shutdown the application"""
        try:
            logging.info("Shutting down banking application")
            
            # Clear current user session
            self.current_user = None
            self.is_admin = False
            
            # Close database connection if needed
            if hasattr(self.db, 'close'):
                self.db.close()
                
            logging.info("Banking application shutdown complete")
            
        except Exception as e:
            logging.error(f"Error during shutdown: {str(e)}")

    def get_user_balance(self, account_number: str) -> float:
        """Get current balance for a user account"""
        try:
            user = self.user_service.get_user_by_account(account_number)
            return user['balance'] if user else 0.0
        except Exception as e:
            logging.error(f"Error getting balance for {account_number}: {str(e)}")
            return 0.0

    def refresh_current_user(self):
        """Refresh current user data from database"""
        if self.current_user and self.current_user.get('account_number'):
            try:
                updated_user = self.user_service.get_user_by_account(
                    self.current_user['account_number']
                )
                if updated_user:
                    self.current_user.update(updated_user)
                    logging.info(f"Refreshed user data for {self.current_user['account_number']}")
            except Exception as e:
                logging.error(f"Error refreshing user data: {str(e)}")

    def validate_transaction_amount(self, amount: float) -> tuple[bool, str]:
        """Validate transaction amount"""
        if amount <= 0:
            return False, "Amount must be positive"
        
        if amount > 1000000:  # 1 million limit
            return False, "Amount exceeds maximum transaction limit"
        
        # Check for reasonable decimal places (max 2)
        if round(amount, 2) != amount:
            return False, "Amount cannot have more than 2 decimal places"
        
        return True, "Valid amount"

    def validate_account_number(self, account_number: str) -> tuple[bool, str]:
        """Validate account number format"""
        if not account_number:
            return False, "Account number cannot be empty"
        
        if len(account_number) != 10:
            return False, "Account number must be exactly 10 digits"
        
        if not account_number.isdigit():
            return False, "Account number must contain only digits"
        
        return True, "Valid account number"

    def perform_deposit(self, account_number: str, amount: float) -> tuple[bool, str]:
        """Perform deposit operation with validation"""
        try:
            # Validate amount
            is_valid, message = self.validate_transaction_amount(amount)
            if not is_valid:
                return False, message
            
            # Perform deposit
            self.transaction_service.deposit(account_number, amount)
            
            # Update current user balance if it's the same user
            if (self.current_user and 
                self.current_user.get('account_number') == account_number):
                self.current_user['balance'] += amount
            
            logging.info(f"Deposit successful: {account_number} - ₱{amount:.2f}")
            return True, f"Successfully deposited ₱{amount:.2f}"
            
        except Exception as e:
            logging.error(f"Deposit failed: {account_number} - {str(e)}")
            return False, f"Deposit failed: {str(e)}"

    def perform_withdrawal(self, account_number: str, amount: float) -> tuple[bool, str]:
        """Perform withdrawal operation with validation"""
        try:
            # Validate amount
            is_valid, message = self.validate_transaction_amount(amount)
            if not is_valid:
                return False, message
            
            # Check balance
            current_balance = self.get_user_balance(account_number)
            if amount > current_balance:
                return False, "Insufficient balance"
            
            # Perform withdrawal
            self.transaction_service.withdraw(account_number, amount)
            
            # Update current user balance if it's the same user
            if (self.current_user and 
                self.current_user.get('account_number') == account_number):
                self.current_user['balance'] -= amount
            
            logging.info(f"Withdrawal successful: {account_number} - ₱{amount:.2f}")
            return True, f"Successfully withdrew ₱{amount:.2f}"
            
        except Exception as e:
            logging.error(f"Withdrawal failed: {account_number} - {str(e)}")
            return False, f"Withdrawal failed: {str(e)}"

    def perform_transfer(self, from_account: str, to_account: str, amount: float) -> tuple[bool, str]:
        """Perform transfer operation with validation"""
        try:
            # Validate amount
            is_valid, message = self.validate_transaction_amount(amount)
            if not is_valid:
                return False, message
            
            # Validate recipient account
            is_valid, message = self.validate_account_number(to_account)
            if not is_valid:
                return False, f"Invalid recipient account: {message}"
            
            # Check if accounts are different
            if from_account == to_account:
                return False, "Cannot transfer to the same account"
            
            # Check if recipient exists
            recipient = self.user_service.get_user_by_account(to_account)
            if not recipient:
                return False, "Recipient account not found"
            
            # Check if recipient account is approved
            if not recipient.get('is_approved', False):
                return False, "Recipient account is not approved"
            
            # Check sender balance
            current_balance = self.get_user_balance(from_account)
            if amount > current_balance:
                return False, "Insufficient balance"
            
            # Perform transfer
            self.transaction_service.transfer(from_account, to_account, amount)
            
            # Update current user balance if it's the sender
            if (self.current_user and 
                self.current_user.get('account_number') == from_account):
                self.current_user['balance'] -= amount
            
            logging.info(f"Transfer successful: {from_account} -> {to_account} - ₱{amount:.2f}")
            return True, f"Successfully transferred ₱{amount:.2f} to {to_account}"
            
        except Exception as e:
            logging.error(f"Transfer failed: {from_account} -> {to_account} - {str(e)}")
            return False, f"Transfer failed: {str(e)}"


def main():
    """Main entry point"""
    app = None
    try:
        print("Initializing IRNVault Banking System...")
        app = BankingApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        if app:
            app.shutdown()
        sys.exit(0)
        
    except Exception as e:
        print(f"Critical application error: {str(e)}")
        logging.critical(f"Critical application error: {str(e)}")
        if app:
            app.shutdown()
        sys.exit(1)
        
    finally:
        if app:
            app.shutdown()


if __name__ == "__main__":
    main()