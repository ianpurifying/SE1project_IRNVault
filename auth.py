import bcrypt
from database import Database

class Auth:
    def __init__(self, db: Database):
        self.db = db

    def hash_pin(self, pin: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pin.encode(), salt)

    def verify_pin(self, pin: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(pin.encode(), hashed)

    def login(self, account_number: str, pin: str) -> bool:
        self.db.connect()
        query = "SELECT hashed_pin FROM accounts WHERE account_number = %s AND is_approved = 1"
        self.db.cursor.execute(query, (account_number,))
        row = self.db.cursor.fetchone()
        self.db.close()
        if row and self.verify_pin(pin, row[0].encode()):
            return True
        return False