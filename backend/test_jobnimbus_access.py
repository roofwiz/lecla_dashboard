from app.config import settings
import requests
import json

def test_jn():
    token = settings.JOB_NIMBUS_TOKEN
    if not token:
        print("❌ No JobNimbus Token found in settings.")
        return

    print(f"🔑 Token loaded (len={len(token)})")
    
    # Endpoint: /jobs or /contacts? Usually /jobs for sales.
    url = "https://app.jobnimbus.com/api1/jobs?limit=5"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"🌍 Fetching: {url}")
    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f"   Status: {res.status_code}")
        
        if res.status_code == 200:
            data = res.json()
            # API might return list directly or {"results": ...}
            if isinstance(data, dict) and 'results' in data:
                items = data['results']
            elif isinstance(data, list):
                items = data
            else:
                items = []
                
            print(f"   Items Found: {len(items)}")
            if items:
                print("\n--- SAMPLE JOB ---")
                print(json.dumps(items[0], indent=2))
        else:
            print(f"   Error: {res.text[:200]}")
            
    except Exception as e:
        print(f"   Exception: {e}")

if __name__ == "__main__":
    test_jn()
