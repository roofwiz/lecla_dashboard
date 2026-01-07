import os
import json
from google.oauth2 import service_account
from google.cloud import aiplatform

SERVICE_ACCOUNT_FILE = "backend/service_account.json"

def location_check():
    print("Checking locations...")
    try:
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        # Use location list directly
        from google.cloud import aiplatform_v1
        # Test basic project call
        print(f"Project: {credentials.project_id}")
        
    except Exception as e:
        print(f"LOCATION CHECK FAILED: {e}")

if __name__ == "__main__":
    location_check()
