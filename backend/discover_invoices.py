import asyncio
from app.services.jobnimbus import jn_client
import httpx

async def run():
    print("Testing /invoices pagination")
    base_url = jn_client.base_url
    headers = jn_client.headers
    
    async with httpx.AsyncClient() as client:
        # Page 1
        resp1 = await client.get(f"{base_url}/invoices?limit=1&skip=0", headers=headers)
        data1 = resp1.json()
        if not data1.get('results'):
            print("No invoices found")
            return
            
        id1 = data1['results'][0]['jnid']
        print(f"Page 1 ID: {id1}")
        
        # Page 2
        resp2 = await client.get(f"{base_url}/invoices?limit=1&skip=1", headers=headers)
        data2 = resp2.json()
        if not data2.get('results'):
            print("No invoices on page 2")
            return
            
        id2 = data2['results'][0]['jnid']
        print(f"Page 2 ID: {id2}")
        
        if id1 == id2:
            print("PAGINATION BROKEN (skip ignored)")
        else:
            print("PAGINATION WORKS")

if __name__ == "__main__":
    asyncio.run(run())
