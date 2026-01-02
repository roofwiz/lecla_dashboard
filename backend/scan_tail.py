from app.config import settings
import pickle
from googleapiclient.discovery import build

def scan_tail():
    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)

    service = build('sheets', 'v4', credentials=creds)

    print("🔍 Inspecting LAST rows of 'Reporting Data'...")
    results = service.spreadsheets().values().get(
        spreadsheetId=settings.GOOGLE_SHEET_ID,
        range="'Reporting Data'!A:K" # Open range to get all
    ).execute()
    
    rows = results.get('values', [])
    count = len(rows)
    print(f"Total Rows: {count}")
    
    print("\n--- LAST 5 ROWS ---")
    start = max(0, count - 5)
    for i in range(start, count):
        r = rows[i]
        # Print Date Created (Col 7, Index 7) and Signed (Col 8, Index 8)
        created = r[7] if len(r)>7 else ""
        signed = r[8] if len(r)>8 else ""
        dname = r[0] if len(r)>0 else ""
        print(f"Row {i+1}: {dname} | Created: {created} | Signed: {signed}")

scan_tail()
