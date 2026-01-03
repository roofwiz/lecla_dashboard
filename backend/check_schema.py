import sqlite3
import sys

def check_schema():
    conn = sqlite3.connect('backend/lecla.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(budgets)")
    columns = cursor.fetchall()
    print("--- Budgets Table Columns ---")
    for col in columns:
        print(f"{col[1]} ({col[2]})")
    
    conn.close()

def check_date_created():
    conn = sqlite3.connect('backend/lecla.db')
    cursor = conn.cursor()
    # Fetch data column
    cursor.execute("SELECT data FROM budgets LIMIT 5")
    rows = cursor.fetchall()
    
    import json
    print("\n--- Budget Date Created Samples ---")
    for row in rows:
        data = json.loads(row[0])
        print(f"Created: {data.get('date_created')} (Timestamp)")

    conn.close()

if __name__ == "__main__":
    check_schema()
    check_date_created()
