import sqlite3
import pandas as pd
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import get_db

def generate_final_report():
    with get_db() as conn:
        print("\n=== EVAN KATZ - FINAL 2025 SALES REPORT ===\n")
        
        start_2025 = 1735689600
        
        # SQL: Fetch Job, Budget Info, and Estimate Info to flag dates
        query = f"""
        SELECT 
            j.name as 'Job Name',
            
            -- Budget Info (The "Sale" Value)
            (SELECT SUM(revenue) FROM budgets 
             WHERE related_job_id = j.jnid 
             AND sales_rep LIKE '%Evan Katz%'
             AND json_extract(data, '$.date_created') >= {start_2025}
            ) as 'Sales Amount',
            
            (SELECT MIN(json_extract(data, '$.date_created')) FROM budgets 
             WHERE related_job_id = j.jnid 
             AND sales_rep LIKE '%Evan Katz%'
             AND json_extract(data, '$.date_created') >= {start_2025}
            ) as 'Budget Date',

            -- Estimate Info (For Validation)
            (SELECT MIN(date_updated) FROM estimates 
             WHERE related_job_id = j.jnid 
             AND status_name IN ('Approved', 'Invoiced')
            ) as 'Date Signed',
            
            (SELECT SUM(total) FROM estimates 
             WHERE related_job_id = j.jnid 
             AND status_name IN ('Approved', 'Invoiced')
            ) as 'Est Amount'
            
        FROM jobs j
        WHERE 
            -- Include if there is a 2025 Budget match
            j.jnid IN (
                SELECT related_job_id FROM budgets 
                WHERE sales_rep LIKE '%Evan Katz%' 
                AND json_extract(data, '$.date_created') >= {start_2025}
            )
        ORDER BY 'Budget Date' ASC
        """
        
        df = pd.read_sql_query(query, conn)
        
        # Convert Timestamps to Strings
        df['Sale Date'] = pd.to_datetime(df['Budget Date'], unit='s').dt.strftime('%Y-%m-%d')
        df['Signed Date'] = pd.to_datetime(df['Date Signed'], unit='s').dt.strftime('%Y-%m-%d')
        
        # Flag Inaccuracies
        # 1. Signed in 2024? (If Signed Date < 2025-01-01)
        df['Signed Year'] = pd.to_datetime(df['Date Signed'], unit='s').dt.year
        df['Notes'] = df['Signed Year'].apply(lambda x: "Signed in 2024 (Possible Carryover)" if x == 2024 else "")
        
        # Select and Rename Columns for Clean Report
        report = df[['Job Name', 'Sales Amount', 'Sale Date', 'Signed Date', 'Notes']].copy()
        report = report.sort_values(by='Sale Date')
        
        # Formatting
        pd.options.display.float_format = '${:,.2f}'.format
        
        # Save to CSV
        csv_path = "backend/Evan_Katz_2025_Sales_Report.csv"
        report.to_csv(csv_path, index=False)
        
        print(f"Report Generated: {csv_path}")
        print("\n--- Preview ---")
        print(report.head(10).to_string(index=False))
        
        # Calculation for Summary
        total_sales = report['Sales Amount'].sum()
        potential_2024 = report[report['Notes'].str.contains('2024')]['Sales Amount'].sum()
        
        print("\n--- SUMMARY ---")
        print(f"Total Sales (2025 Budgets):       ${total_sales:,.2f}")
        print(f"Flagged as 'Signed in 2024':    -${potential_2024:,.2f}")
        print(f"Adjusted (Strictly 2025 Signed): ${total_sales - potential_2024:,.2f}")

if __name__ == "__main__":
    generate_final_report()
