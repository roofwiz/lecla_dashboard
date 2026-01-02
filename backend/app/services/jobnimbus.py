from app.config import settings
import httpx
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class JobNimbusClient:
    def __init__(self):
        self.base_url = "https://app.jobnimbus.com/api1"
        self.token = settings.JOB_NIMBUS_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    async def get_jobs_simple(self, limit: int = 50):
        url = f"{self.base_url}/jobs?limit={limit}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self.headers, timeout=30.0)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, dict) and 'results' in data:
                    return data['results']
                return data
            else:
                logger.error(f"JN Error {resp.status_code}: {resp.text}")
                return []

    async def fetch_all_jobs(self, year_filter: int = None):
        """Fetch ALL jobs, optionally filtering by year (client-side filter for now)."""
        all_jobs = []
        limit = 1000
        skip = 0
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            while True:
                url = f"{self.base_url}/jobs?limit={limit}&skip={skip}"
                logger.info(f"Fetching JN Jobs: skip={skip}")
                try:
                    resp = await client.get(url, headers=self.headers)
                    if resp.status_code != 200:
                        logger.error(f"JN API Error: {resp.text}")
                        break
                        
                    data = resp.json()
                    results = []
                    if isinstance(data, dict) and 'results' in data:
                        results = data['results']
                    elif isinstance(data, list):
                        results = data
                    
                    if not results:
                        break
                        
                    all_jobs.extend(results)
                    skip += len(results)
                    
                    if len(results) < limit:
                        break
                        
                except Exception as e:
                    logger.error(f"JN Exception: {e}")
                    break
        
        return all_jobs

jn_client = JobNimbusClient()
