import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Accounts (
                id INTEGER PRIMARY KEY,
                Name TEXT,
                Email TEXT,
                Password TEXT
            )
        """)
        self.connection.commit()

    def fetch(self):
        self.cursor.execute("""
            SELECT * FROM Accounts
        """)
        rows = self.cursor.fetchall()
        return rows

    def insert(self, name, email, password):
        self.cursor.execute("""
            INSERT OR IGNORE INTO Accounts VALUES (NULL, ?, ?, ?)
        """, (name, email, password))
        self.connection.commit()

    def remove(self, Id):
        self.cursor.execute("""
                    DELETE FROM Accounts WHERE id=?
                """, (Id,))
        self.connection.commit()

    def update(self, Id, name, email, password):
        self.cursor.execute("""
             UPDATE Accounts SET 
             Name = ?,
             Email = ?,
             Password = ?
             WHERE id = ?
         """, (name, email, password, Id))
        self.connection.commit()

    def __del__(self):
        self.connection.close


