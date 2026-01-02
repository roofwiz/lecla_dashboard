from app.config import settings
import pickle
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def verify_sheets():
    print("Verifying Google Sheets Access...")
    
    if not os.path.exists("backend/token.pickle"):
        print("❌ Error: backend/token.pickle not found.")
        print("   Please run 'python backend/google_auth_flow.py' and complete the login.")
        return

    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("❌ Error: Credentials invalid.")
            return

    try:
        service = build('sheets', 'v4', credentials=creds)
        
        # 1. Get Spreadsheet Metadata
        print(f"📄 connecting to Sheet ID: {settings.GOOGLE_SHEET_ID}")
        sheet_metadata = service.spreadsheets().get(spreadsheetId=settings.GOOGLE_SHEET_ID).execute()
        properties = sheet_metadata.get('properties', {})
        sheets = sheet_metadata.get('sheets', [])
        
        print(f"✅ CONNECTION SUCCESSFUL!")
        print(f"Title: {properties.get('title')}")
        print(f"Found {len(sheets)} tabs/sheets:")
        
        for sheet in sheets:
            title = sheet['properties']['title']
            print(f"  - {title}")

    except Exception as e:
        print(f"❌ API Error: {str(e)}")

def verify_drive():
    print("\nVerifying Google Drive Access...")
    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)
        
    try:
        service = build('drive', 'v3', credentials=creds)
        
        # 0. Check Identity
        about = service.about().get(fields="user").execute()
        user = about.get('user', {})
        print(f"👤 Authenticated as: {user.get('displayName')} <{user.get('emailAddress')}>")
        print(f"   (Please ensure the Sheet is shared with THIS email)\n")

        # Search for the folders user mentioned
        print("🔍 Searching for 'Marketing' and 'Documents' folders...")
        
        # Added supportsAllDrives=True to search Shared Drives too
        results = service.files().list(
            q="mimeType = 'application/vnd.google-apps.folder' and (name contains 'Marketing' or name contains 'Document') and trashed = false",
            pageSize=10,
            fields="nextPageToken, files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        files = results.get('files', [])
        if files:
            print(f"✅ Found {len(files)} folders:")
            for f in files:
                print(f"  - {f['name']} (ID: {f['id']})")
        else:
            print("⚠️ No matching folders found (Check exact names).")

    except Exception as e:
        print(f"❌ API Error: {str(e)}")

if __name__ == "__main__":
    verify_sheets()
    verify_drive()
