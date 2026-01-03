import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import get_db

def run():
    with get_db() as conn:
        c = conn.cursor()
        
        # Check counts
        tables = ['jobs', 'budgets', 'estimates', 'invoices']
        for t in tables:
            try:
                c.execute(f"SELECT count(*) FROM {t}")
                print(f"{t}: {c.fetchone()[0]}")
            except Exception as e:
                print(f"{t}: Error {e}")
        
        # Create indices
        print("Creating indices...")
        c.execute("CREATE INDEX IF NOT EXISTS idx_invoices_related ON invoices(related_job_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_estimates_related ON estimates(related_job_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_budgets_related ON budgets(related_job_id)")
        conn.commit()
        print("Indices created.")

if __name__ == "__main__":
    run()
