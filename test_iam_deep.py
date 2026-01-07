import os
import json
from google.oauth2 import service_account
from googleapiclient import discovery

SERVICE_ACCOUNT_FILE = "backend/service_account.json"

def test_iam():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, 
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        project_id = credentials.project_id
        email = credentials.service_account_email
        
        # Test if we can list the IAM policy (basic check)
        service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
        policy = service.projects().getIamPolicy(resource=project_id).execute()
        
        print(f"Checking IAM for {email} in {project_id}")
        found = False
        for binding in policy.get('bindings', []):
            if f"serviceAccount:{email}" in binding.get('members', []):
                print(f"Found Role: {binding.get('role')}")
                found = True
        
        if not found:
            print("ERROR: Service account not found in project IAM policy!")

    except Exception as e:
        print(f"IAM TEST FAILED: {str(e)}")

if __name__ == "__main__":
    test_iam()
