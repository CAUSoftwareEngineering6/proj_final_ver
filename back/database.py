import sqlite3

class Database:
    def __init__(self, db_path='SWE.db'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.connection.commit()

    def query(self, query, params=None):
        self.cursor.execute(query, params or ())

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def lastrowid(self):
        return self.cursor.lastrowid

    def __del__(self):
        self.cursor.close()
        self.connection.close()