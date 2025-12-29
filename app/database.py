import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables to get DB_PATH
load_dotenv()
DB_PATH = os.getenv("DB_PATH", "members.db")

def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    Using 'row_factory' allows us to access columns by name (row['email'])
    instead of just index (row[2]).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This is the secret sauce for easy data access
    return conn

def init_db():
    """
    Initializes the database table if it doesn't exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the members table
    # We use IF NOT EXISTS so this script is safe to run multiple times
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            join_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at: {DB_PATH}")

if __name__ == "__main__":
    # If we run this file directly, it initializes the DB
    init_db()