import sqlite3
import os
import sys
import asyncio

# Fix path for imports
sys.path.append(os.getcwd())

from backend.app.db import DB_PATH, init_db
from backend.crm_sync import full_sync

def reset_db():
    print(f"Dropping existing tables in {DB_PATH}...")
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Drop all relevant tables
        c.execute("DROP TABLE IF EXISTS jobs")
        c.execute("DROP TABLE IF EXISTS contacts")
        c.execute("DROP TABLE IF EXISTS leads")
        c.execute("DROP TABLE IF EXISTS budgets")
        c.execute("DROP TABLE IF EXISTS estimates")
        c.execute("DROP TABLE IF EXISTS invoices")
        conn.commit()
        conn.close()
        print("Tables dropped.")
    else:
        print("Database file not found. Nothing to drop.")

async def main():
    reset_db()
    print("Re-initializing database schema...")
    init_db()
    print("Schema initialized.")
    print("Running full sync to populate CRM data...")
    await full_sync()
    print("Migration and Sync completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
