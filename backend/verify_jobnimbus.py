import requests
from app.config import settings
import json

def test_connection():
    # JobNimbus API Endpoint
    # Checking both potential base URLs often cited in docs to be safe
    # But usually api1 is for keys
    base_url = "https://app.jobnimbus.com/api1"
    endpoint = f"{base_url}/contacts"
    
    print(f"Testing connection to: {endpoint}")
    
    headers = {
        "Authorization": f"Bearer {settings.JOB_NIMBUS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Try to fetch just 1 contact to keep it light
    params = {"limit": 1}
    
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ CONNECTION SUCCESSFUL!")
            data = response.json()
            # detailed print
            print(f"Found {len(data.get('results', []))} contacts in sample.")
            if len(data.get('results', [])) > 0:
                print("First contact name:", data['results'][0].get('display_name') or data['results'][0].get('first_name'))
        else:
            print("❌ CONNECTION FAILED")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    if not settings.JOB_NIMBUS_TOKEN or settings.JOB_NIMBUS_TOKEN == "xxxxxxxxxxxxx":
         print("❌ Error: API Token not set properly in .env")
    else:
        test_connection()
