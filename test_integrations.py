import asyncio
import httpx
from backend.app.config import settings
from backend.app.services.companycam import cc_client

async def test_cc():
    print(f"Testing CompanyCam with token: {settings.COMPANY_CAM_TOKEN[:5]}...")
    projects = await cc_client.get_projects()
    print(f"Projects found: {len(projects)}")
    if projects:
        print(f"First project: {projects[0].get('name')}")
    else:
        # Check if the token is valid by making a direct call
        headers = {"Authorization": f"Bearer {settings.COMPANY_CAM_TOKEN}"}
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.companycam.com/v2/projects", headers=headers)
            print(f"Direct call status: {r.status_code}")
            print(f"Direct call response: {r.text[:200]}")

async def test_ai():
    print(f"Testing AI with key: {settings.VERTEX_AI_KEY[:5]}...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.VERTEX_AI_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": "Hello, who are you?"}]
        }]
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload)
        print(f"AI status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            try:
                text = data['candidates'][0]['content']['parts'][0]['text']
                print(f"AI Response: {text}")
            except:
                print(f"Structure issue: {data}")
        else:
            print(f"AI Error: {r.text}")

if __name__ == "__main__":
    asyncio.run(test_cc())
    asyncio.run(test_ai())
