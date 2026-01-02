import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

BASE_DIR = Path(__file__).resolve().parent

def main():
    creds = None
    token_path = BASE_DIR / 'token.pickle'
    secret_path = BASE_DIR / 'client_secret.json'
    
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not secret_path.exists():
                print(f"❌ Error: {secret_path} not found.")
                print("   Please ensure 'client_secret.json' is in the backend/ directory.")
                return

            flow = InstalledAppFlow.from_client_secrets_file(
                str(secret_path), SCOPES)
            
            print("\n" + "="*60)
            print("🚀  GOOGLE AUTHENTICATION STARTED")
            print("="*60)
            print("1. A link will appear below (start with https://...)")
            print("2. COPY that link.")
            print("3. PASTE it into your WEB BROWSER (Chrome/Edge).")
            print("4. DO NOT PASTE IT HERE IN THE TERMINAL!")
            print("5. Log in, then come back here.")
            print("="*60 + "\n")

            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
            print("✅ Authentication successful! token.pickle saved.")

if __name__ == '__main__':
    main()
