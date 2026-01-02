from app.config import settings
import pickle
from googleapiclient.discovery import build

def inspect_report():
    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)

    service = build('drive', 'v3', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)

    print("🔍 Searching for 'Report' files...")
    # Search for anything with 'Report' in name
    results = service.files().list(
        q="name contains 'Report' or name contains 'report'",
        fields="files(id, name, mimeType)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    
    files = results.get('files', [])
    
    print(f"\nFound {len(files)} files matching 'Report':")
    for f in files:
        print(f" - [{f['mimeType']}] {f['name']} (ID: {f['id']})")
        
        # If it looks like the one we want, read headers
        if "spreadsheet" in f['mimeType'] and "Performance" in f['name']:
            print("   >>> READING HEADERS <<<")
            try:
                resp = sheets_service.spreadsheets().values().get(
                    spreadsheetId=f['id'],
                    range="A1:Z2"
                ).execute()
                rows = resp.get('values', [])
                for i, row in enumerate(rows):
                    print(f"   Row {i}: {row}")
            except Exception as e:
                print(f"   (Read Error: {e})")
    print("\n")

if __name__ == "__main__":
    inspect_report()
