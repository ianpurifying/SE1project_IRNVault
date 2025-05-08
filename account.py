import random
from database import Database

class AccountManager:
    def __init__(self, db: Database):
        self.db = db

    def generate_account_number(self) -> str:
        return str(random.randint(10**9, 10**10 - 1))

    def register(self, name: str, pin_hash: bytes, initial_balance: float = 0.0):
        acct_no = self.generate_account_number()
        self.db.connect()
        query = "INSERT INTO accounts (account_number, name, hashed_pin, balance, is_approved) VALUES (%s, %s, %s, %s, 0)"
        self.db.cursor.execute(query, (acct_no, name, pin_hash.decode(), initial_balance))
        self.db.commit()
        self.db.close()
        print(f"Account {acct_no} registered. Awaiting admin approval.")