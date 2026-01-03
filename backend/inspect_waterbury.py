import sqlite3
import pandas as pd
import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import get_db

def inspect_waterbury():
    with get_db() as conn:
        # Search for Waterbury in Jobs
        query = """
        SELECT 
            j.name as 'Job Name',
            j.jnid as 'Job ID',
            j.total as 'Job Total',
            datetime(j.date_updated, 'unixepoch') as 'Job Updated',
            b.number as 'Budget #',
            b.revenue as 'Budget Rev',
            b.sales_rep as 'Sales Rep',
            i.number as 'Invoice #',
            i.total as 'Inv Total',
            i.fees as 'Inv Fees',
            datetime(i.date_created, 'unixepoch') as 'Inv Created'
        FROM jobs j
        LEFT JOIN budgets b ON b.related_job_id = j.jnid
        LEFT JOIN invoices i ON i.related_job_id = j.jnid
        WHERE j.name LIKE '%Waterbury%'
        ORDER BY j.name
        """
        df = pd.read_sql_query(query, conn)
        
        print("\n--- Waterbury Jobs ---")
        if not df.empty:
            df.to_csv("backend/waterbury_jobs.csv", index=False)
            print("Saved to backend/waterbury_jobs.csv")
        else:
            print("No jobs found with 'Waterbury' in the name.")

        # Check Evan Katz stats for 2025 (based on Inv Created or Budget Updated?)
        # User said "budgets created in 2025" or "estimates signed in 2025".
        # We assume 2025 is >= 1735689600 (Jan 1 2025).
        # Actually JobNimbus uses seconds, so 1735689600.
        
        print("\n--- Evan Katz 2025 Preview (Based on Budgets Updated in 2025) ---")
        query_evan = """
        SELECT 
            b.number, b.revenue, b.sales_rep, j.name, 
            datetime(b.date_updated, 'unixepoch') as updated
        FROM budgets b
        JOIN jobs j ON b.related_job_id = j.jnid
        WHERE b.sales_rep LIKE '%Evan Katz%'
        AND b.date_updated >= 1735689600
        """
        df_evan = pd.read_sql_query(query_evan, conn)
        print(df_evan.to_string())

if __name__ == "__main__":
    inspect_waterbury()
