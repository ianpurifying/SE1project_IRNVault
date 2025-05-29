import sys
from auth import Auth
from account import AccountManager
from transaction import TransactionManager
from history import History
from admin import Admin
from database import Database



class Menu:
    ADMIN_ACCT_NO = '0000000001'

    def __init__(self):
        self.db = Database()
        self.auth = Auth(self.db)
        self.acct_mgr = AccountManager(self.db)
        self.txn_mgr = TransactionManager(self.db)
        self.admin = Admin(self.db)

    def main_menu(self):
        while True:
            print("\n=== IRNVault Main Menu ===")
            print("1. Register   2. Login   3. Exit")
            choice = input("Select: ")
            if choice == '1':
                self.register_flow()
            elif choice == '2':
                self.login_flow()
            elif choice == '3':
                print("Exiting. Goodbye!")
                sys.exit()
            else:
                print("Invalid option. Please choose 1-3.")

    def register_flow(self):
        print("\n--- Account Registration ---")
        name = input("Enter your full name: ")
        while True:
            pin = input("Enter a 6-digit PIN: ")
            if not pin.isdigit() or len(pin) != 6:
                print("Error: PIN must be exactly 6 digits and numeric. Try again.")
                continue
            break
        pin_hash = self.auth.hash_pin(pin)
        self.acct_mgr.register(name, pin_hash)

    def login_flow(self):
        print("\n--- Account Login ---")
        acct_no = input("Account Number: ")
        pin = input("PIN: ")
        # Admin case
        if acct_no == self.ADMIN_ACCT_NO:
            self._admin_login(pin, acct_no)
            return
        # Normal user
        if not self.auth.login(acct_no, pin):
            print("Login failed. Check credentials or approval status.")
            return
        print(f"Login successful. Welcome, {acct_no}!")
        self._user_menu(acct_no)

    def _admin_login(self, pin: str, acct_no: str):
        self.db.connect()
        self.db.cursor.execute(
            "SELECT hashed_pin FROM accounts WHERE account_number = %s",
            (acct_no,)
        )
        row = self.db.cursor.fetchone()
        self.db.close()
        if not row or not self.auth.verify_pin(pin, row[0].encode()):
            print("Login failed. Check credentials.")
            return
        print(f"Admin login detected ({acct_no}). Redirecting to Admin Dashboard...")
        self._admin_menu()

    def _user_menu(self, acct_no: str):
        while True:
            print("\n--- Account Menu ---")
            print("1. Deposit   2. Withdraw   3. Transfer   4. Balance   5. Mini Statement   6. Logout")
            choice = input("Select: ")
            if choice == '1':
                amount = float(input("Amount to deposit: "))
                self.txn_mgr.deposit(acct_no, amount)
            elif choice == '2':
                amount = float(input("Amount to withdraw: "))
                self.txn_mgr.withdraw(acct_no, amount)
            elif choice == '3':
                target = input("Target account number: ")
                amount = float(input("Amount to transfer: "))
                self.txn_mgr.transfer(acct_no, target, amount)
            elif choice == '4':
                self.db.connect()
                self.db.cursor.execute(
                    "SELECT balance FROM accounts WHERE account_number = %s", (acct_no,)
                )
                balance = self.db.cursor.fetchone()[0]
                self.db.close()
                print(f"Current balance: {balance}")
            elif choice == '5':
                self.history.mini_statement(acct_no)
            elif choice == '6':
                print("Logging out...")
                break
            else:
                print("Invalid selection. Choose 1-6.")

    def _admin_menu(self):
        while True:
            print("\n=== Admin Dashboard ===")
            print("1. Pending Accounts   2. Display Users   3. Logout")
            choice = input("Select: ")
            if choice == '1':
                self._admin_pending()
            elif choice == '2':
                self._admin_display_users()
            elif choice == '3':
                print("Admin logging out...")
                break
            else:
                print("Invalid option. Please choose 1-3.")

    def _admin_pending(self):
        pending = self.admin.list_pending()
        if not pending:
            print("No pending accounts to review.")
            return
        print("\nPending Accounts:")
        for acct_no, name in pending:
            print(f"- {acct_no} : {name}")
        acct = input("Enter account number to process (or press Enter to cancel): ")
        if not acct:
            return
        action = input("Approve (A) or Decline (D)? ").strip().upper()
        if action == 'A':
            self.admin.approve(acct)
        elif action == 'D':
            reason = input("Reason for decline: ")
            self.admin.decline(acct, reason)
        else:
            print("Invalid choice. Returning.")

    def _admin_display_users(self):
        print("\nSorted By:")
        print("1. Balance (Least to Most)   2. Name")
        choice = input("Select: ")
        if choice == '1':
            users = self.admin.list_users(order_by='balance')
        elif choice == '2':
            users = self.admin.list_users(order_by='name')
        else:
            print("Invalid choice. Returning.")
            return
        if not users:
            print("No users found.")
            return
        print("\nUsers:")
        for acct_no, name, balance in users:
            print(f"- {acct_no} | Balance: {balance} | {name}")
        to_del = input("Enter account number to delete (or press Enter to skip): ")
        if to_del:
            confirm = input(f"Confirm delete {to_del}? (Y/N): ").strip().upper()
            if confirm == 'Y':
                self.admin.delete_user(to_del)
            else:
                print("Deletion canceled.")