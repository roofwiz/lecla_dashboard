from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.routers import google, reports, calendar
from backend.app.services.jobnimbus import jn_client
import os
import pickle
from datetime import datetime

app = FastAPI(title="Lecla Dashboard API")

# Include Routers
app.include_router(google.router, prefix="/api/google", tags=["google"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["calendar"])

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
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
    print("✅ Job Nimbus API Token loaded" if settings.JOB_NIMBUS_TOKEN else "❌ Job Nimbus Token missing")
    print("✅ Company Cam Token loaded" if settings.COMPANY_CAM_TOKEN else "❌ Company Cam Token missing")
    print("✅ Google API Key loaded" if settings.GOOGLE_API_KEY else "⚠️ Google API Key missing or empty")
    
    if settings.GOOGLE_TOKEN_PICKLE.exists():
        print("✅ Google Token (OAuth) found")
    else:
        print("⚠️ Google Token (OAuth) NOT found. Run google_auth_flow.py")
        
    print("✅ Google Sheet ID configured" if settings.GOOGLE_SHEET_ID else "❌ Google Sheet ID missing")

@app.get("/")
def read_root():
    return {"message": "Lecla Dashboard API is running"}

@app.get("/api/jobs")
async def proxy_jobs(limit: int = 50):
    try:
        # Optimization: Only fetch jobs from the last 6 months for the dashboard
        six_months_ago = int(datetime.now().timestamp() - (180 * 24 * 60 * 60))
        filters = {"date_created_gt": six_months_ago}
        
        results = await jn_client.get_jobs_simple(limit=limit, extra_params=filters)
        return results
    except Exception as e:
        print(f"Proxy Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects")
async def proxy_projects(limit: int = 25):
    # Reuse Jobs logic for now
    return await proxy_jobs(limit)
