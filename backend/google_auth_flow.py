import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
            print("✅ Authentication successful! token.pickle saved.")

if __name__ == '__main__':
    main()
