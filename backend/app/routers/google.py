from fastapi import APIRouter, HTTPException
from backend.app.config import settings
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

router = APIRouter()

def get_google_creds():
    creds = None
    token_path = settings.GOOGLE_TOKEN_PICKLE
    
    if token_path.exists():
        try:
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"Error loading google tokens: {e}")
            raise HTTPException(status_code=500, detail="Could not load Google tokens")
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                # This is a blocking network call. 
                # Since this function is called inside synchronous route handlers, 
                # FastAPI will run them in a thread pool, which is fine.
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing google tokens: {e}")
                raise HTTPException(status_code=401, detail=f"Google token refresh failed: {str(e)}")
        else:
             raise HTTPException(status_code=401, detail="Google Not Authorized. Server needs to re-authenticate.")
    return creds

@router.get("/sheet")
def get_sheet_data():
    """
    Fetch all data from the configured Google Sheet.
    Returns a dictionary where keys are sheet titles and values are lists of rows.
    """
    creds = get_google_creds()
    start_time = None
    
    try:
        service = build('sheets', 'v4', credentials=creds)
        
        # 1. Get Spreadsheet Metadata to find all sheet titles
        sheet_metadata = service.spreadsheets().get(spreadsheetId=settings.GOOGLE_SHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', [])
        
        result = {}
        
        # 2. Iterate over each sheet and fetch data
        for sheet in sheets:
            title = sheet['properties']['title']
            # Fetch all data from this sheet (assuming reasonable size)
            range_name = f"'{title}'!A1:Z1000" 
            response = service.spreadsheets().values().get(
                spreadsheetId=settings.GOOGLE_SHEET_ID,
                range=range_name
            ).execute()
            
            rows = response.get('values', [])
            result[title] = rows
            
        return result
        
    except Exception as e:
        print(f"Google Sheets Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/drive")
def get_drive_folders(query: str = ""):
    """
    Search for folders/files in Google Drive.
    """
    creds = get_google_creds()
    try:
        service = build('drive', 'v3', credentials=creds)
        
        # Basic search query
        q = "mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        if query:
            q += f" and name contains '{query}'"
            
        results = service.files().list(
            q=q,
            pageSize=10, 
            fields="nextPageToken, files(id, name)"
        ).execute()
        
        return results.get('files', [])
    except Exception as e:
         print(f"Google Drive Error: {str(e)}")
         raise HTTPException(status_code=500, detail=str(e))
