from app.config import settings
import pickle
from googleapiclient.discovery import build

def scan_share_folder():
    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)

    service = build('drive', 'v3', credentials=creds)

    print("🔍 Searching for 'Shared to Share' folder...")
    results = service.files().list(
        q="mimeType = 'application/vnd.google-apps.folder' and name = 'Shared to Share'",
        fields="files(id, name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    
    folders = results.get('files', [])
    
    if not folders:
        print("❌ Folder 'Shared to Share' not found. Please ensure it is shared with the authenticated email.")
        return

    folder_id = folders[0]['id']
    print(f"✅ Found Folder: {folders[0]['name']} (ID: {folder_id})")
    
    # List contents
    print("\n📂 Folder Contents:")
    files_result = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    
    files = files_result.get('files', [])
    print(f"\nFound {len(files)} files:")
    for f in files:
        # Simplify Mime
        mime = "FOLDER" if "folder" in f['mimeType'] else "FILE"
        if "spreadsheet" in f['mimeType']: mime = "SHEET"
        if "document" in f['mimeType']: mime = "DOC"
        
        print(f" - {mime:<8} {f['name']}")

if __name__ == "__main__":
    scan_share_folder()
