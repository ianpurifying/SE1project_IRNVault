from decimal import Decimal
from database import Database

class TransactionManager:
    def __init__(self, db: Database):
        self.db = db

    def deposit(self, account_number: str, amount: float):
        self.db.connect()
        try:
            # Lock row for update
            self.db.cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s FOR UPDATE",
                (account_number,)
            )
            balance: Decimal = self.db.cursor.fetchone()[0]
            # Convert to Decimal
            amt = Decimal(str(amount))
            new_balance = balance + amt

            # Update balance
            self.db.cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_number = %s",
                (new_balance, account_number)
            )
            # Log transaction
            self.db.cursor.execute(
                "INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'deposit', %s)",
                (account_number, amt)
            )
            self.db.commit()
            print(f"Deposited {amt}. New balance: {new_balance}")
        except Exception as e:
            self.db.rollback()
            print(f"Transaction failed: {e}")
        finally:
            self.db.close()

    def withdraw(self, account_number: str, amount: float):
        self.db.connect()
        try:
            self.db.cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s FOR UPDATE",
                (account_number,)
            )
            balance: Decimal = self.db.cursor.fetchone()[0]
            amt = Decimal(str(amount))
            if amt > balance:
                raise ValueError("Insufficient funds")
            new_balance = balance - amt

            self.db.cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_number = %s",
                (new_balance, account_number)
            )
            self.db.cursor.execute(
                "INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'withdrawal', %s)",
                (account_number, amt)
            )
            self.db.commit()
            print(f"Withdrew {amt}. New balance: {new_balance}")
        except Exception as e:
            self.db.rollback()
            print(f"Transaction failed: {e}")
        finally:
            self.db.close()

    def transfer(self, from_acct: str, to_acct: str, amount: float):
        self.db.connect()
        try:
            amt = Decimal(str(amount))

            # Withdraw from source
            self.db.cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s FOR UPDATE",
                (from_acct,)
            )
            src_balance: Decimal = self.db.cursor.fetchone()[0]
            if amt > src_balance:
                raise ValueError("Insufficient funds for transfer")
            new_src = src_balance - amt
            self.db.cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_number = %s",
                (new_src, from_acct)
            )

            # Deposit to target
            self.db.cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s FOR UPDATE",
                (to_acct,)
            )
            tgt_balance: Decimal = self.db.cursor.fetchone()[0]
            new_tgt = tgt_balance + amt
            self.db.cursor.execute(
                "UPDATE accounts SET balance = %s WHERE account_number = %s",
                (new_tgt, to_acct)
            )

            # Log both halves
            self.db.cursor.execute(
                "INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'transfer_out', %s)",
                (from_acct, amt)
            )
            self.db.cursor.execute(
                "INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'transfer_in', %s)",
                (to_acct, amt)
            )

            self.db.commit()
            print(f"Transferred {amt} from {from_acct} to {to_acct}.")
        except Exception as e:
            self.db.rollback()
            print(f"Transfer failed: {e}")
        finally:
            self.db.close()
