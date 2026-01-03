import sqlite3
import pandas as pd
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import get_db

def run_audit():
    with get_db() as conn:
        start_2025 = 1735689600
        
        print("\n=== Evan Katz 2025 Audit ===\n")
        
        # 1. Estimates Signed (Approved/Invoiced) in 2025
        print("--- Estimates (Approved/Invoiced in 2025) ---")
        query_est = f"""
        SELECT 
            e.number as 'Est #', 
            j.name as 'Job Name',
            e.total as 'Total', 
            e.status_name as 'Status',
            datetime(e.date_updated, 'unixepoch') as 'Date Updated'
        FROM estimates e
        LEFT JOIN jobs j ON e.related_job_id = j.jnid
        WHERE j.data LIKE '%Evan Katz%' 
        AND e.status_name IN ('Approved', 'Invoiced')
        AND e.date_updated >= {start_2025}
        ORDER BY e.date_updated DESC
        """
        df_est = pd.read_sql_query(query_est, conn)
        if not df_est.empty:
            print(df_est.to_string(index=False))
            print(f"Total Signed Estimates: ${df_est['Total'].sum():,.2f}")
        else:
            print("No estimates found.")

        # 2. Budgets Updated in 2025
        print("\n--- Budgets (Updated in 2025) ---")
        query_bud = f"""
        SELECT 
            b.number as 'Budget #', 
            j.name as 'Job Name',
            b.revenue as 'Revenue', 
            datetime(b.date_updated, 'unixepoch') as 'Date Updated'
        FROM budgets b
        LEFT JOIN jobs j ON b.related_job_id = j.jnid
        WHERE b.sales_rep = 'Evan Katz'
        AND b.date_updated >= {start_2025}
        ORDER BY b.date_updated DESC
        """
        df_bud = pd.read_sql_query(query_bud, conn)
        if not df_bud.empty:
            print(df_bud.to_string(index=False))
            print(f"Total Budget Revenue: ${df_bud['Revenue'].sum():,.2f}")
        else:
            print("No budgets found.")

        # 3. Waterbury Breakdown
        print("\n--- The Waterbury Job Issue ---")
        waterbury_job_id = 'lzle1t6joycdp4929r4pzoy'
        
        # Budgets for Waterbury
        q_w_bud = f"SELECT number, revenue FROM budgets WHERE related_job_id = '{waterbury_job_id}'"
        df_w_bud = pd.read_sql_query(q_w_bud, conn)
        
        # Invoices for Waterbury
        q_w_inv = f"SELECT number, total, datetime(date_created, 'unixepoch') as date FROM invoices WHERE related_job_id = '{waterbury_job_id}'"
        df_w_inv = pd.read_sql_query(q_w_inv, conn)
        
        print("Budgets Linked to Job:")
        print(df_w_bud.to_string(index=False))
        print(f"Total Budgets: ${df_w_bud['revenue'].sum():,.2f}")
        
        print("\nInvoices Linked to Job:")
        print(df_w_inv.to_string(index=False))
        print(f"Total Invoices: ${df_w_inv['total'].sum():,.2f}")
        
        print("\nISSUE: The Job '380 Old Waterbury' has multiple Budgets and multiple Invoices attached to the SAME Job ID.")
        print("Standard reports compare EACH Budget against the SUM of ALL Invoices, causing triple-counting of the invoice total in discrepancies.")

if __name__ == "__main__":
    run_audit()
