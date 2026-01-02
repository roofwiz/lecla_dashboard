from app.config import settings
import pickle
from googleapiclient.discovery import build

def scan_jobs():
    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)

    service = build('sheets', 'v4', credentials=creds)

    print("🔍 Inspecting 'Jobs' Tab...")
    # Read Header
    res_head = service.spreadsheets().values().get(
        spreadsheetId=settings.GOOGLE_SHEET_ID,
        range="'Jobs'!A1:Z1"
    ).execute()
    header = res_head.get('values', [[]])[0]
    print(f"Headers: {header}")

    # Read All to find Last
    results = service.spreadsheets().values().get(
        spreadsheetId=settings.GOOGLE_SHEET_ID,
        range="'Jobs'!A:A" # Just Col A to count rows
    ).execute()
    
    rows = results.get('values', [])
    count = len(rows)
    print(f"Total Rows in Jobs: {count}")
    
    if count > 1:
        # Read last 5 full rows
        start = max(1, count - 5)
        rng = f"'Jobs'!A{start}:Z{count}"
        res_tail = service.spreadsheets().values().get(
            spreadsheetId=settings.GOOGLE_SHEET_ID,
            range=rng
        ).execute()
        tail_rows = res_tail.get('values', [])
        
        print("\n--- LAST 5 ROWS ---")
        for i, tr in enumerate(tail_rows):
            print(f"Row {start+i}: {tr}")

scan_jobs()
