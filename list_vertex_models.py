import os
import vertexai
from google.oauth2 import service_account
from google.cloud import aiplatform

SERVICE_ACCOUNT_FILE = "backend/service_account.json"

def list_models():
    try:
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        aiplatform.init(project=credentials.project_id, location="us-central1", credentials=credentials)
        
        print("Available models in us-central1:")
        models = aiplatform.Model.list()
        if not models:
            print("No models found via Model.list().")
        for m in models:
            print(f" - {m.display_name} ({m.resource_name})")
            
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    list_models()
