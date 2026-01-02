from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
import httpx
import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

app = FastAPI(title="Lecla Dashboard API")

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Job Nimbus
    if settings.JOB_NIMBUS_TOKEN:
        print("✅ Job Nimbus API Token loaded")
    else:
        print("⚠️ Job Nimbus API Token missing")
    
    # Company Cam
    if settings.COMPANY_CAM_TOKEN:
        print("✅ Company Cam Token loaded")
    else:
        print("⚠️ Company Cam Token missing")

    # Google
    if settings.GOOGLE_API_KEY:
        print("✅ Google API Key loaded")
    else:
        print("⚠️ Google API Key missing or empty")
        
    if settings.GOOGLE_TOKEN_PICKLE.exists():
        print("✅ Google Calendar Token found")
    else:
        print("⚠️ Google Calendar Token missing (Run google_auth_flow.py)")

@app.get("/")
def read_root():
    return {"message": "Welcome to Lecla Dashboard API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/jobs")
async def get_jobs(limit: int = 10):
    """
    Proxy endpoint to fetch jobs from Job Nimbus
    """
    if not settings.JOB_NIMBUS_TOKEN:
         raise HTTPException(status_code=500, detail="Job Nimbus Token not configured")

    url = "https://app.jobnimbus.com/api1/jobs"
    headers = {
        "Authorization": f"Bearer {settings.JOB_NIMBUS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params={"limit": limit})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Job Nimbus API Error: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch jobs from Job Nimbus")
        except Exception as e:
            print(f"Internal Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects")
async def get_projects(limit: int = 25):
    """
    Proxy endpoint to fetch projects from CompanyCam
    """
    if not settings.COMPANY_CAM_TOKEN:
         raise HTTPException(status_code=500, detail="Company Cam Token not configured")

    url = "https://api.companycam.com/v2/projects"
    headers = {
        "Authorization": f"Bearer {settings.COMPANY_CAM_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params={"per_page": limit})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Company Cam API Error: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch projects from CompanyCam")
        except Exception as e:
            print(f"Internal Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/calendar")
def get_calendar_events(limit: int = 10):
    """
    Fetch upcoming events from Google Calendar
    """
    creds = None
    token_path = settings.GOOGLE_TOKEN_PICKLE
    
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
             raise HTTPException(status_code=401, detail="Google Calendar Not Authorized. Server needs to re-authenticate.")

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        import datetime
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print(f"Fetching calendar events from {now}...")
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=limit, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        return events
        
    except Exception as e:
        print(f"Google Calendar Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
