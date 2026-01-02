from app.config import settings
import pickle
from googleapiclient.discovery import build

def sample_sheet_data():
    creds = None
    with open("backend/token.pickle", 'rb') as token:
        creds = pickle.load(token)

    try:
        service = build('sheets', 'v4', credentials=creds)
        
        # We'll look at "Reporting Data" and "Reporting Table" and "Jobs" 
        # to see which one has the sales rep data.
        tabs_to_check = ["Reporting Data", "Reporting Table", "Jobs"]
        
        for tab in tabs_to_check:
            print(f"\n--- TAB: {tab} ---")
            range_name = f"'{tab}'!A1:Z2"  # Just header and one data row
            response = service.spreadsheets().values().get(
                spreadsheetId=settings.GOOGLE_SHEET_ID,
                range=range_name
            ).execute()
            rows = response.get('values', [])
            
            if len(rows) > 0:
                print(f"HEADERS ({len(rows[0])} cols):")
                for i, header in enumerate(rows[0]):
                    print(f"  [{i}] {header}")
            
            if len(rows) > 1:
                print("ROW 1 SAMPLE (First 5):", rows[1][:5])
            else:
                print("No data rows found.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sample_sheet_data()
