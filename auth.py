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

    def check_account_declined(self, account_number: str) -> tuple[bool, str]:
        """
        Check if account is in the declined accounts table.
        Returns (is_declined, reason) tuple.
        """
        self.db.connect()
        query = "SELECT reason FROM account_declines WHERE account_number = %s"
        self.db.cursor.execute(query, (account_number,))
        row = self.db.cursor.fetchone()
        self.db.close()
        
        if row:
            return True, row[0]  # Account is declined, return reason
        return False, ""  # Account is not declined

    def login(self, account_number: str, pin: str) -> tuple[bool, str]:
        """
        Attempt to login with account number and PIN.
        Returns (success, message) tuple.
        """
        # First check if account is declined
        is_declined, decline_reason = self.check_account_declined(account_number)
        if is_declined:
            return False, f"Login denied. Account declined: {decline_reason}"
        
        # Proceed with normal login flow
        self.db.connect()
        query = "SELECT hashed_pin FROM accounts WHERE account_number = %s AND is_approved = 1"
        self.db.cursor.execute(query, (account_number,))
        row = self.db.cursor.fetchone()
        self.db.close()
        
        if row and self.verify_pin(pin, row[0].encode()):
            return True, "Login successful"
        return False, "Login failed. Check credentials or approval status."