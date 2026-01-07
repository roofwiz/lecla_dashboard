import os
import json
from google.oauth2 import service_account
import google.auth
import google.auth.transport.requests

SERVICE_ACCOUNT_FILE = "backend/service_account.json"

def check_identity():
    try:
        with open(SERVICE_ACCOUNT_FILE, 'r') as f:
            data = json.load(f)
            print(f"File Project ID: {data.get('project_id')}")
            print(f"File Email: {data.get('client_email')}")

        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/cloud-platform'])
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        
        print(f"Token present: {credentials.token is not None}")
        
        # Check current project from auth
        from google.cloud import resourcemanager_v3
        client = resourcemanager_v3.ProjectsClient(credentials=credentials)
        project = client.get_project(name=f"projects/{data.get('project_id')}")
        print(f"Project Display Name: {project.display_name}")
        print(f"Project State: {project.state}")

    except Exception as e:
        print(f"IDENTITY CHECK FAILED: {str(e)}")

if __name__ == "__main__":
    check_identity()
