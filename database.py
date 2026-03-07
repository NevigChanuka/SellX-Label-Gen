import sqlite3

class Database:
    def __init__(self, db_name="labels.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS customers 
                            (name TEXT PRIMARY KEY, address TEXT, city TEXT, phone1 TEXT, phone2 TEXT)''')
        self.conn.commit()

    def get_suggestions(self, query):
        self.cursor.execute("SELECT name FROM customers WHERE name LIKE ?", (f"{query}%",))
        return [row[0] for row in self.cursor.fetchall()]

    def get_customer(self, name):
        self.cursor.execute("SELECT * FROM customers WHERE name=?", (name,))
        return self.cursor.fetchone()

    def save_customer(self, data):
        self.cursor.execute("REPLACE INTO customers VALUES (?, ?, ?, ?, ?)", data)
        self.conn.commit()
        
    def delete_customer(self, name):
        self.cursor.execute("DELETE FROM customers WHERE name=?", (name,))
        self.conn.commit()