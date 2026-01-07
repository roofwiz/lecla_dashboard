import os
from google.oauth2 import service_account
from googleapiclient import discovery

SERVICE_ACCOUNT_FILE = "backend/service_account.json"

def check_api_status():
    try:
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        service = discovery.build('serviceusage', 'v1', credentials=credentials)
        
        project_id = credentials.project_id
        name = f'projects/{project_id}/services/aiplatform.googleapis.com'
        
        print(f"Checking status for: {name}")
        request = service.services().get(name=name)
        response = request.execute()
        
        print(f"API State: {response.get('state')}")
        
    except Exception as e:
        print(f"FAILED TO CHECK API STATUS: {str(e)}")

if __name__ == "__main__":
    check_api_status()
