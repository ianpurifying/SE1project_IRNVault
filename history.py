from database import Database

class History:
    def __init__(self, db: Database):
        self.db = db

    def mini_statement(self, account_number: str, limit: int = 5):
        self.db.connect()
        query = "SELECT timestamp, type, amount FROM transactions WHERE account_number = %s ORDER BY timestamp DESC LIMIT %s"
        self.db.cursor.execute(query, (account_number, limit))
        rows = self.db.cursor.fetchall()
        self.db.close()
        print("Mini Statement:")
        for ts, ttype, amt in rows:
            print(f"{ts}: {ttype} {amt}")