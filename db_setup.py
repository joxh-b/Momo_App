import sqlite3
from parser import parse_xml

DB_FILE = "momo_transactions.db"
XML_FILE = "modified_sms_v2.xml"

# Create the database and table
def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            date TEXT,
            reference TEXT,
            type TEXT,
            message TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Insert transactions into the database
def insert_transactions():
    transactions = parse_xml(XML_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for tx in transactions:
        cursor.execute("""
            INSERT INTO transactions (amount, date, reference, type, message)
            VALUES (?, ?, ?, ?, ?)
        """, (tx["amount"], tx["date"], tx["reference"], tx["type"], tx["message"]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    insert_transactions()
    print("Database setup complete and data inserted.")
