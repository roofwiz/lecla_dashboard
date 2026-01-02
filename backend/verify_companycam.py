import requests
from app.config import settings
import json

def test_companycam():
    url = "https://api.companycam.com/v2/projects"
    
    print(f"Testing connection to: {url}")
    
    token = settings.COMPANY_CAM_TOKEN
    masked = f"{token[:5]}...{token[-5:]}" if len(token) > 10 else "Too Short"
    print(f"Token Loaded: {masked} (Len: {len(token)})")

    headers = {
        "Authorization": f"Bearer {settings.COMPANY_CAM_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Fetch 1 project
    params = {"per_page": 1}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ CONNECTION SUCCESSFUL!")
            data = response.json()
            if len(data) > 0:
                print(f"Found project: {data[0].get('name')} (ID: {data[0].get('id')})")
            else:
                print("Connection successful, but no projects found.")
        else:
            print("❌ CONNECTION FAILED")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    if not settings.COMPANY_CAM_TOKEN:
         print("❌ Error: Company Cam Token not set in .env")
    else:
        test_companycam()
