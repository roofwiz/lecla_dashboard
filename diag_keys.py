import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')
cc_token = os.getenv('COMPANY_CAM_TOKEN')
vertex_key = os.getenv('VERTEX_AI_API_KEY') or os.getenv('Vertex_AI_API_Key')

async def check():
    print(f"CC Token: {cc_token[:5]}...")
    headers = {"Authorization": f"Bearer {cc_token}"}
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.companycam.com/v2/projects?per_page=1", headers=headers)
        print(f"CC Status: {r.status_code}")
        if r.status_code == 200:
            print(f"CC Project: {r.json()[0].get('name')}")
        else:
            print(f"CC Error: {r.text}")

    print(f"Vertex Key: {vertex_key[:5]}...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={vertex_key}"
    payload = {"contents": [{"parts": [{"text": "hi"}]}]}
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload)
        print(f"Vertex AI Status: {r.status_code}")
        if r.status_code != 200:
            print(f"Vertex AI Error: {r.text}")

asyncio.run(check())
