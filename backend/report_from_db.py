import sqlite3
import pandas as pd
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import get_db

def generate_report():
    query = """
    SELECT 
        datetime(b.date_updated, 'unixepoch') as 'Budget Updated',
        b.number as 'Budget #',
        b.sales_rep as 'Sales Rep',
        b.revenue as 'Budget Rev',
        
        j.name as 'Job Name',
        datetime(j.date_updated, 'unixepoch') as 'Job Updated',
        j.total as 'Job Total',
        
        (SELECT SUM(total) FROM estimates WHERE related_job_id = j.jnid) as 'Est Total',
        
        datetime((SELECT MAX(date_created) FROM invoices WHERE related_job_id = j.jnid), 'unixepoch') as 'Last Inv Date',
        (SELECT SUM(total) FROM invoices WHERE related_job_id = j.jnid) as 'Inv Total',
        (SELECT SUM(fees) FROM invoices WHERE related_job_id = j.jnid) as 'Inv Fees',
        
        IFNULL((SELECT SUM(total) FROM invoices WHERE related_job_id = j.jnid), 0) - 
        IFNULL((SELECT SUM(fees) FROM invoices WHERE related_job_id = j.jnid), 0) as 'Adj Inv Revenue',
        
        (b.revenue - (IFNULL((SELECT SUM(total) FROM invoices WHERE related_job_id = j.jnid), 0) - 
                      IFNULL((SELECT SUM(fees) FROM invoices WHERE related_job_id = j.jnid), 0))) as 'Discrepancy'
    FROM budgets b
    LEFT JOIN jobs j ON b.related_job_id = j.jnid
    WHERE ABS(b.revenue - j.total) > 1.0 
       OR ABS(Discrepancy) > 1.0
    ORDER BY ABS(Discrepancy) DESC
    """
    
    with get_db() as conn:
        df = pd.read_sql_query(query, conn)
        
    if not df.empty:
        print(f"Found {len(df)} discrepancies.")
        print(df.head(10))
        df.to_csv("backend/discrepancy_report_db.csv", index=False)
        print("Report saved to backend/discrepancy_report_db.csv")
    else:
        print("No discrepancies found (or database empty).")

if __name__ == "__main__":
    generate_report()
