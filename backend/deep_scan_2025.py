from app.config import settings
import pickle
from googleapiclient.discovery import build
import re
from datetime import datetime

# Helpers copied from reports.py
def parse_currency(value_str):
    if not value_str: return 0.0
    if isinstance(value_str, (int, float)): return float(value_str)
    # Remove $ and ,
    clean = re.sub(r'[^\d.-]', '', str(value_str))
    try:
        return float(clean)
    except:
        return 0.0

def parse_date(date_str):
    if not date_str: return None
    # Add your date parsing logic here (e.g. Month DD, YYYY or MM/DD/YYYY)
    formats = [
        "%B %d, %Y", # "June 2, 2025"
        "%m/%d/%Y",  # "6/2/2025"
        "%Y-%m-%d"   # "2025-06-02"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str).strip(), fmt)
        except ValueError:
            continue
    return None

def deep_scan():
    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)

    service = build('sheets', 'v4', credentials=creds)

    print("🔍 Deep Scan of 'Reporting Data' for 2025 High Value Jobs...")
    results = service.spreadsheets().values().get(
        spreadsheetId=settings.GOOGLE_SHEET_ID,
        range="'Reporting Data'!A2:K"
    ).execute()
    
    rows = results.get('values', [])
    print(f"Total Rows Found: {len(rows)}")
    
    # ... rest of logic uses new parse_date/currency ...
    
    high_value_count = 0
    in_2025_count = 0
    missed_2025_count = 0
    
    print("\nSample High Value Rows (> $5,000):")
    print(f"{'Row':<5} | {'Created':<12} | {'Signed':<12} | {'Revenue':<12} | {'Status'}")
    print("-" * 70)
    
    for i, row in enumerate(rows):
        if len(row) <= 9: continue
        
        status = row[2] if len(row) > 2 else ""
        date_created = row[7] if len(row) > 7 else ""
        date_signed = row[8] if len(row) > 8 else ""
        budget_raw = row[9] if len(row) > 9 else "0"
        invoice_raw = row[10] if len(row) > 10 else "0"
        
        rev = max(parse_currency(budget_raw), parse_currency(invoice_raw))
        
        dt_c = parse_date(date_created)
        dt_s = parse_date(date_signed)
        effective = dt_s if dt_s else dt_c
        
        # Stats
        if effective and effective.year == 2025:
            in_2025_count += 1
        elif rev > 5000:
             # Excluded High Value Jobs
             reason = "Visited 2024/Other"
             if not effective: reason = "No Valid Date"
             elif effective.year != 2025: reason = f"Year {effective.year}"
             
             print(f"❌ EXCLUDED Row {i+2}: Rev=${rev:,.0f} | Created='{date_created}' Signed='{date_signed}' | {reason}")

    print("-" * 70)
    print(f"Total Jobs in 2025 (Detected): {in_2025_count}")

if __name__ == "__main__":
    deep_scan()
