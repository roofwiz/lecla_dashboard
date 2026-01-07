import os
import json
from google.oauth2 import service_account
from google.cloud import aiplatform

SERVICE_ACCOUNT_FILE = "backend/service_account.json"

def simple_diag():
    print("Starting simple diag...")
    try:
        with open(SERVICE_ACCOUNT_FILE, 'r') as f:
            data = json.load(f)
            project_id = data.get('project_id')
            print(f"Project in JSON: {project_id}")

        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        aiplatform.init(project=project_id, location="us-central1", credentials=credentials)
        
        print("Checking if we can list models (proves API and project ID are correct)...")
        # Just listing models doesn't generate content but proves identity and API enablement
        models = aiplatform.Model.list(filter='display_name="gemini-1.5-flash"')
        print(f"Success! Models found: {len(models)}")
        for m in models:
            print(f" - Model: {m.display_name} ({m.resource_name})")

    except Exception as e:
        print(f"DIAG FAILED: {e}")

if __name__ == "__main__":
    simple_diag()
