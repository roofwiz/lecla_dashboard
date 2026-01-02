from app.config import settings
import requests

token = settings.COMPANY_CAM_TOKEN
print(f"Token Repr: {repr(token)}")

headers = {"Authorization": f"Bearer {token}"}
r = requests.get("https://api.companycam.com/v2/projects", headers=headers, params={"limit": 1})
print(r.status_code)
print(r.text)
