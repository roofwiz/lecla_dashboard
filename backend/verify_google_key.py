import requests
from app.config import settings

def test_google_maps():
    print("Testing Google Maps Geocoding API...")
    
    key = settings.GOOGLE_API_KEY
    if not key or "your_key" in key:
        print("❌ ERROR: GOOGLE_API_KEY is missing or invalid in .env")
        return

    # Test address: 1600 Amphitheatre Parkway, Mountain View, CA
    # This is free/cheap to test usually.
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": "1600 Amphitheatre Parkway, Mountain View, CA",
        "key": key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "OK":
            print("✅ CONNECTION SUCCESSFUL!")
            result = data["results"][0]
            print(f"Formatted Address: {result.get('formatted_address')}")
            print(f"Lat/Lng: {result['geometry']['location']}")
        else:
            print("❌ CONNECTION FAILED")
            print(f"Status: {data.get('status')}")
            print(f"Error Message: {data.get('error_message')}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_google_maps()
