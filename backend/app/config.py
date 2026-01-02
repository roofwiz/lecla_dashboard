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
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID", "")
    
    GOOGLE_CLIENT_SECRET: Path = BASE_DIR / "client_secret.json"
    GOOGLE_TOKEN_PICKLE: Path = BASE_DIR / "token.pickle"

settings = Settings()
