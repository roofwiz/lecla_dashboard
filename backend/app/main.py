from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.routers import google, reports, calendar, crm, auth, ai, tasks, workflows, custom_fields, financials
from backend.app.services.jobnimbus import jn_client
from backend.app.services.companycam import cc_client
from backend.app.database import get_db as get_sqlalchemy_db
from backend.app.models import Job, Base
from sqlalchemy.orm import Session
from fastapi import Depends
import os
import pickle
from datetime import datetime
from backend.app.database import engine
from backend.app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lecla Dashboard API")

# Include Routers
app.include_router(google.router, prefix="/api/google", tags=["google"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["calendar"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(crm.router, prefix="/api/crm", tags=["crm"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(custom_fields.router, prefix="/api/custom-fields", tags=["custom-fields"])
app.include_router(financials.router, prefix="/api/financials", tags=["financials"])

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
    print("🚀 Starting Lecla Dashboard API...")
    print("✅ Job Nimbus API Token loaded" if settings.JOB_NIMBUS_TOKEN else "❌ Job Nimbus Token missing")
    print("✅ Company Cam Token loaded" if settings.COMPANY_CAM_TOKEN else "❌ Company Cam Token missing")
    print("✅ Google API Key loaded" if settings.GOOGLE_API_KEY else "⚠️ Google API Key missing or empty")
    
    if settings.GOOGLE_TOKEN_PICKLE.exists():
        print("✅ Google Token (OAuth) found")
    else:
        print("⚠️ Google Token (OAuth) NOT found. Run google_auth_flow.py")
        
    print("✅ Google Sheet ID configured" if settings.GOOGLE_SHEET_ID else "❌ Google Sheet ID missing")
    print("🚀 API fully initialized and ready to serve.")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Lecla Dashboard API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/config")
async def get_config():
    """Expose necessary public configuration to the frontend."""
    return {
        "google_maps_api_key": settings.GOOGLE_API_KEY
    }

@app.get("/api/jobs")
async def proxy_jobs(limit: int = 50, db: Session = Depends(get_sqlalchemy_db)):
    try:
        # Optimization: Fetch from local DB first (much faster)
        jobs = db.query(Job).order_by(Job.date_created.desc()).limit(limit).all()
        if jobs:
            return jobs
            
        # Fallback to API if DB is empty
        six_months_ago = int(datetime.now().timestamp() - (180 * 24 * 60 * 60))
        filters = {"date_created_gt": six_months_ago}
        results = await jn_client.get_jobs_simple(limit=limit, extra_params=filters)
        return results
    except Exception as e:
        print(f"Proxy Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects")
async def proxy_projects(limit: int = 25):
    """Fetch active projects from CompanyCam."""
    return await cc_client.get_projects(per_page=limit)

@app.get("/api/photos")
async def proxy_photos(project_id: str = None, limit: int = 20):
    """Fetch recent photos from CompanyCam projects."""
    if project_id:
        return await cc_client.get_project_photos(project_id, per_page=limit)
    
    # If no project ID, get latest projects and their photos? 
    # For now, let's just support project-specific or return empty
    return []
