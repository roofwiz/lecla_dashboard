import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    JOB_NIMBUS_TOKEN: str = os.getenv("JOB_NIMBUS_API_TOKEN", "")
    COMPANY_CAM_TOKEN: str = os.getenv("COMPANY_CAM_TOKEN", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_MAPS_PLATFORM_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID", "")
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "lecla-dashboard")
    GCP_LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    GCP_SERVICE_ACCOUNT_JSON: Path = BASE_DIR / "service_account.json"
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/lecla.db")
    
    GOOGLE_CLIENT_SECRET: Path = BASE_DIR / "client_secret.json"
    GOOGLE_TOKEN_PICKLE: Path = BASE_DIR / "token.pickle"

settings = Settings()
