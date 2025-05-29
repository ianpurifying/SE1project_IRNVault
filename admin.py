from database import Database

class Admin:
    ADMIN_ACCT_NO = '0000000001'
    
    def __init__(self, db: Database):
        self.db = db

    def list_pending(self):
        self.db.connect()
        self.db.cursor.execute(
            "SELECT account_number, name FROM accounts WHERE is_approved = 0"
        )
        pending = self.db.cursor.fetchall()
        self.db.close()
        return pending

    def approve(self, account_number: str):
        self.db.connect()
        self.db.cursor.execute(
            "UPDATE accounts SET is_approved = 1 WHERE account_number = %s",
            (account_number,)
        )
        self.db.commit()
        self.db.close()
        print(f"Account {account_number} approved.")

    def decline(self, account_number: str, reason: str):
        self.db.connect()
        self.db.cursor.execute(
            "INSERT INTO account_declines (account_number, reason) VALUES (%s, %s)",
            (account_number, reason)
        )
        self.db.cursor.execute(
            "UPDATE accounts SET is_approved = -1 WHERE account_number = %s",
            (account_number,)
        )
        self.db.commit()
        self.db.close()
        print(f"Account {account_number} declined: {reason}")

    def list_users(self, order_by: str = 'balance'):
        # order_by can be 'balance' or 'name'
        valid = {'balance': 'balance', 'name': 'name'}
        col = valid.get(order_by, 'balance')
        self.db.connect()
        self.db.cursor.execute(
            f"SELECT account_number, name, balance FROM accounts WHERE is_approved = 1 ORDER BY {col} ASC"
        )
        users = self.db.cursor.fetchall()
        self.db.close()
        return users

    def delete_user(self, account_number: str):
        # Prevent deletion of the admin account
        if account_number == self.ADMIN_ACCT_NO:
            print(f"Error: Cannot delete admin account {account_number}.")
            return

        self.db.connect()
        self.db.cursor.execute(
            "DELETE FROM accounts WHERE account_number = %s",
            (account_number,)
        )
        self.db.commit()
        self.db.close()
        print(f"Account {account_number} has been deleted.")


