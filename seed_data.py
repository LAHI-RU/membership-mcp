from app.database import get_db_connection, init_db
from datetime import datetime, timedelta

def seed_database():
    # Ensure table exists first
    init_db()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # clear existing data to avoid duplicates during testing
    cursor.execute("DELETE FROM members")
    
    # Helper to format dates
    today = datetime.now()
    days_ago_30 = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    days_future_10 = (today + timedelta(days=10)).strftime("%Y-%m-%d")
    days_future_60 = (today + timedelta(days=60)).strftime("%Y-%m-%d")
    last_year = (today - timedelta(days=365)).strftime("%Y-%m-%d")

    members = [
        # Expired member
        ("Alice Expired", "alice@example.com", last_year, days_ago_30, "active"),
        # Expiring VERY soon (within 30 days)
        ("Bob Soon", "bob@example.com", last_year, days_future_10, "active"),
        # Healthy member
        ("Charlie Good", "charlie@example.com", last_year, days_future_60, "active"),
        # Cancelled member
        ("Dave Cancelled", "dave@example.com", last_year, days_future_60, "cancelled")
    ]
    
    print("🌱 Seeding data...")
    cursor.executemany('''
        INSERT INTO members (name, email, join_date, expiry_date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', members)
    
    conn.commit()
    conn.close()
    print("✅ Dummy data inserted successfully!")

if __name__ == "__main__":
    seed_database()