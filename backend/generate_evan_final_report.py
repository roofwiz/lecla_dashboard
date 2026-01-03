import sqlite3
import pandas as pd
import sys
import os
import json
from datetime import datetime

# Setup path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import get_db

def generate_report():
    with get_db() as conn:
        print("Fetching data for Evan Katz Final Report...")
        
        query = """
        SELECT 
            j.name as JobName,
            j.jnid as JobID,
            
            -- Budgets
            b.bud_revenue,
            b.bud_date_created,
            
            -- Estimates
            e.est_total,
            e.est_date_signed
            
        FROM jobs j
        
        LEFT JOIN (
            SELECT 
                related_job_id, 
                SUM(revenue) as bud_revenue, 
                MIN(json_extract(data, '$.date_created')) as bud_date_created
            FROM budgets 
            WHERE sales_rep LIKE '%Evan Katz%'
            GROUP BY related_job_id
        ) b ON j.jnid = b.related_job_id
        
        LEFT JOIN (
            SELECT 
                related_job_id, 
                SUM(total) as est_total, 
                MIN(date_updated) as est_date_signed
            FROM estimates 
            WHERE status_name IN ('Approved', 'Invoiced')
            GROUP BY related_job_id
        ) e ON j.jnid = e.related_job_id
        
        WHERE j.data LIKE '%Evan Katz%'
        AND (b.bud_revenue IS NOT NULL OR e.est_total IS NOT NULL)
        """
        
        df = pd.read_sql_query(query, conn)
        
        if df.empty:
            print("No data found for Evan Katz.")
            return

        # Filters
        start_2025 = 1735689600
        
        # Determine Dates
        df['Budget_Date_DT'] = pd.to_datetime(df['bud_date_created'], unit='s')
        df['Signed_Date_DT'] = pd.to_datetime(df['est_date_signed'], unit='s')
        
        # Filter Logic: IS THIS A 2025 SALE?
        # A) Budget Created in 2025+
        # B) OR Estimate Signed in 2025+
        is_2025_bud = df['bud_date_created'] >= start_2025
        is_2025_est = df['est_date_signed'] >= start_2025
        
        df_2025 = df[is_2025_bud | is_2025_est].copy()
        
        # Calculate Sale Amount
        # Priority: Budget > Estimate
        df_2025['Final_Sale_Amount'] = df_2025['bud_revenue'].fillna(0)
        
        # Use Estimate if Budget is 0 (Draft/Placeholder) or Missing
        mask_use_est = (df_2025['Final_Sale_Amount'] == 0)
        df_2025.loc[mask_use_est, 'Final_Sale_Amount'] = df_2025.loc[mask_use_est, 'est_total']
        
        # Flags for Footnotes / Notes
        df_2025['Notes'] = ""
        
        # Flag 1: Signed in 2024?
        # If Signed Date exists AND is < 2025
        mask_signed_2024 = (df_2025['est_date_signed'].notnull()) & (df_2025['est_date_signed'] < start_2025)
        df_2025.loc[mask_signed_2024, 'Notes'] += "Signed in 2024. "
        
        # Flag 2: No Budget?
        mask_no_budget = (df_2025['bud_revenue'].isnull()) | (df_2025['bud_revenue'] == 0)
        df_2025.loc[mask_no_budget, 'Notes'] += "Estimate Value (No Budget). "
        
        # Format Dates for report
        df_2025['Sale Date'] = df_2025['Budget_Date_DT'].dt.strftime('%Y-%m-%d')
        # If no budget date, use signed date
        df_2025.loc[df_2025['Sale Date'].isnull(), 'Sale Date'] = df_2025['Signed_Date_DT'].dt.strftime('%Y-%m-%d')
        
        df_2025['Signed Date'] = df_2025['Signed_Date_DT'].dt.strftime('%Y-%m-%d')
        
        # Final Columns
        report = df_2025[['JobName', 'Final_Sale_Amount', 'Sale Date', 'Signed Date', 'Notes']].copy()
        report.rename(columns={'JobName': 'Job Name', 'Final_Sale_Amount': 'Sales Amount'}, inplace=True)
        report = report.sort_values(by='Sale Date')
        
        # Formatting
        pd.options.display.float_format = '${:,.2f}'.format
        
        # Save
        path = "backend/Evan_Katz_Final_Report_v3.csv"
        report.to_csv(path, index=False)
        
        print(f"\n--- REPORT SUMMARY ---")
        print(f"Report saved: {path}")
        print(f"Total Sales Identified: ${report['Sales Amount'].sum():,.2f}")
        
        # Inaccuracy Analysis
        signed_2024 = report[report['Notes'].str.contains('2024')]['Sales Amount'].sum()
        est_only = report[report['Notes'].str.contains('Estimate Value')]['Sales Amount'].sum()
        
        print(f"Potential Carryover (Signed 2024): ${signed_2024:,.2f}")
        print(f"Estimated Only (No Budget):        ${est_only:,.2f}")
        print(f"Confirmed 2025 (Budget+Signed):    ${report['Sales Amount'].sum() - signed_2024 - est_only:,.2f}")
        
        # Preview
        print("\n--- Preview (Top 15) ---")
        print(report.head(15).to_string(index=False))

if __name__ == "__main__":
    generate_report()
