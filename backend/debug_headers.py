from app.config import settings
import pickle
from googleapiclient.discovery import build
import sys

# clean output
sys.stdout.reconfigure(encoding='utf-8')

def get_headers():
    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)

    service = build('sheets', 'v4', credentials=creds)
    
    # Inspect Data Rows
    print("\n--- SCANNING FOR VALID SALES (First 500 Rows) ---")
    resp = service.spreadsheets().values().get(
        spreadsheetId=settings.GOOGLE_SHEET_ID, 
        range="'Reporting Data'!A2:J500"
    ).execute()
    
    rows = resp.get('values', [])
    valid_count = 0
    
    print(f"{'IDX':<5} | {'SALES REP':<20} | {'DATE SIGNED':<15} | {'REVENUE':<15}")
    print("-" * 70)

    for i, row in enumerate(rows):
        if len(row) <= 9: continue
        
        rep = row[3]
        date = row[8]
        rev = row[9]
        
        # Check if "Sort of Valid"
        if date and rev != "$0.00" and rev != "0":
            print(f"{i:<5} | {rep[:20]:<20} | {date[:15]:<15} | {rev[:15]:<15}")
            valid_count += 1
            if valid_count >= 10: break
    
    if valid_count == 0:
        print("❌ No rows found with BOTH 'Date Signed' and Revenue > 0")

if __name__ == "__main__":
    get_headers()
