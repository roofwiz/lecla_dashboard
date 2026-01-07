import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'backend' / 'lecla.db'
print(f"Checking database: {db_path}")
print(f"Database exists: {db_path.exists()}")

if db_path.exists():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f"\nExisting tables: {[t[0] for t in tables]}")
    
    # Check jobs table structure
    if 'jobs' in [t[0] for t in tables]:
        cols = cursor.execute("PRAGMA table_info(jobs)").fetchall()
        print(f"\nJobs table columns ({len(cols)}):")
        for col in cols:
            print(f"  - {col[1]} ({col[2]})")
        
        # Count jobs
        count = cursor.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        print(f"\nTotal jobs: {count}")
    else:
        print("\n⚠ Jobs table does not exist!")
    
    conn.close()
