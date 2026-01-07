import os
import vertexai
from google.oauth2 import service_account
from google.cloud import aiplatform

SERVICE_ACCOUNT_FILE = "backend/service_account.json"

def diag():
    try:
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        aiplatform.init(project=credentials.project_id, location="us-east1", credentials=credentials)
        
        print(f"Project: {credentials.project_id}")
        print(f"Email: {credentials.service_account_email}")
        
        print("Attempting to list Vertex AI endpoints (us-east1)...")
        from google.api_core import client_options
        from google.cloud import aiplatform_v1
        
        client = aiplatform_v1.EndpointServiceClient(
            client_options=client_options.ClientOptions(api_endpoint="us-east1-aiplatform.googleapis.com"),
            credentials=credentials
        )
        response = client.list_endpoints(parent=f"projects/{credentials.project_id}/locations/us-east1")
        print("Success! Connectivity to Vertex AI confirmed.")
        
    except Exception as e:
        print(f"DIAG FAILED: {str(e)}")

if __name__ == "__main__":
    diag()
吐
