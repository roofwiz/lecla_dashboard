import os
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# Path to the service account key file
SERVICE_ACCOUNT_FILE = "backend/service_account.json"

def test_vertex_auth():
    print(f"Checking for service account file: {SERVICE_ACCOUNT_FILE}")
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print("ERROR: File not found!")
        return

    try:
        # Load credentials
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        print(f"Active Identity: {credentials.service_account_email}")
        print(f"Active Project: {credentials.project_id}")
        
        # Initialize Vertex AI
        vertexai.init(project=credentials.project_id, location="us-central1", credentials=credentials)
        
        # Initialize the model
        model = GenerativeModel("gemini-1.5-flash")
        
        print("Sending test request to Vertex AI...")
        response = model.generate_content("Say 'Vertex AI is ready!'")
        print(f"Response: {response.text}")
        print("AUTH SUCCESS!")
        
    except Exception as e:
        print(f"AUTH FAILED: {str(e)}")

if __name__ == "__main__":
    test_vertex_auth()
