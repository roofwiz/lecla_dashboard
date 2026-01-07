import httpx
from backend.app.config import settings
import logging

logger = logging.getLogger(__name__)

class CompanyCamClient:
    def __init__(self):
        self.base_url = "https://api.companycam.com/v2"
        self.token = settings.COMPANY_CAM_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    async def get_projects(self, per_page: int = 50):
        url = f"{self.base_url}/projects?per_page={per_page}"
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, headers=self.headers, timeout=30.0)
                if resp.status_code == 200:
                    return resp.json()
                else:
                    logger.error(f"CC Error {resp.status_code}: {resp.text}")
                    return []
            except Exception as e:
                logger.error(f"CC Exception (Projects): {e}")
                return []

    async def get_project_photos(self, project_id: str, per_page: int = 10):
        url = f"{self.base_url}/projects/{project_id}/photos?per_page={per_page}"
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, headers=self.headers, timeout=30.0)
                if resp.status_code == 200:
                    return resp.json()
                else:
                    logger.error(f"CC Error {resp.status_code}: {resp.text}")
                    return []
            except Exception as e:
                logger.error(f"CC Exception (Photos): {e}")
                return []

cc_client = CompanyCamClient()
