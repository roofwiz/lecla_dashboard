from app.config import settings
import pickle
from googleapiclient.discovery import build

def check_status_values():
    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)

    service = build('sheets', 'v4', credentials=creds)

    print("🔍 Checking Status Values in 'Reporting Data'...")
    results = service.spreadsheets().values().get(
        spreadsheetId=settings.GOOGLE_SHEET_ID,
        range="'Reporting Data'!C2:C1000" # Col 3 is Sales Rep? Wait.
        # Header (Step 713): 0: Name, 1: Record Type, 2: Status
        # Col C is Index 2.
    ).execute()
    
    rows = results.get('values', [])
    statuses = {}
    for r in rows:
        if not r: continue
        val = r[0] # First col of range C
        statuses[val] = statuses.get(val, 0) + 1
        
    print("\nUNIQUE STATUSES:")
    for s, count in statuses.items():
        print(f" - {s}: {count}")

if __name__ == "__main__":
    check_status_values()
