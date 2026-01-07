from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from backend.app.database import get_db as get_sqlalchemy_db
from backend.app.models import Contact, Job, Budget
from backend.app.routers.auth import get_current_user, check_role
from sqlalchemy.orm import Session
from sqlalchemy import func
import os

router = APIRouter()

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None

class ContactResponse(ContactBase):
    lecla_id: str
    jn_contact_id: Optional[str] = None
    
    model_config = {"from_attributes": True}

class JobResponse(BaseModel):
    lecla_id: str
    jnid: Optional[str] = None
    number: Optional[str] = None
    name: Optional[str] = None
    status_name: Optional[str] = None
    total: Optional[float] = 0.0
    contact_id: Optional[str] = None
    date_created: Optional[int] = None
    
    model_config = {"from_attributes": True}

@router.get("/contacts", response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_sqlalchemy_db)):
    contacts = db.query(Contact).order_by(Contact.last_name, Contact.first_name).all()
    return contacts

@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: str, db: Session = Depends(get_sqlalchemy_db)):
    contact = db.query(Contact).filter(Contact.lecla_id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.get("/jobs", response_model=List[JobResponse])
async def get_jobs(db: Session = Depends(get_sqlalchemy_db)):
    jobs = db.query(Job).order_by(Job.date_updated.desc()).limit(500).all()
    return jobs

@router.get("/jobs/active", response_model=List[JobResponse])
async def get_active_jobs(db: Session = Depends(get_sqlalchemy_db)):
    """
    Get truly active jobs (15-25 expected)
    
    Criteria:
    - Estimates signed in last 14 days
    - Status in active states
    - Exclude completed/closed jobs
    """
    from datetime import datetime, timedelta
    
    fourteen_days_ago = int((datetime.now() - timedelta(days=14)).timestamp())
    
    # Active statuses that indicate work in progress
    active_statuses = [
        'In Progress',
        'Scheduled', 
        'Materials Ordered',
        'Started',
        'Pending',
        'Approved',
        'Production'
    ]
    
    # Build query for active jobs
    query = db.query(Job).filter(
        (Job.status_name.in_(active_statuses)) |
        (Job.first_estimate_signed_date >= fourteen_days_ago)
    ).filter(
        Job.status_name.notin_(['Paid & Closed', 'Cancelled', 'Lost', 'Void'])
    )
    
    jobs = query.order_by(Job.date_updated.desc()).limit(50).all()
    return jobs

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, db: Session = Depends(get_sqlalchemy_db)):
    job = db.query(Job).filter(Job.lecla_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/audit")
async def get_sales_audit(db: Session = Depends(get_sqlalchemy_db), current_user: dict = Depends(get_current_user)):
    """Fetch budget vs job discrepancies for data quality audit."""
    # Using SQLAlchemy query for better cross-DB support
    results = db.query(
        Budget.number.label('budget_number'),
        Budget.sales_rep,
        Budget.revenue.label('budget_revenue'),
        Job.name.label('job_name'),
        Job.total.label('job_total'),
        Job.jnid.label('related_job_id'),
        (Budget.revenue - Job.total).label('discrepancy')
    ).outerjoin(Job, Budget.related_job_id == Job.jnid)\
     .filter(func.abs(Budget.revenue - Job.total) > 1.0)\
     .order_by(func.abs(Budget.revenue - Job.total).desc())\
     .limit(100).all()
    
    return [r._asdict() for r in results]

@router.post("/sync", tags=["sync"])
async def trigger_sync():
    """Trigger manual sync with JobNimbus in the background."""
    import subprocess
    import os
    
    # Run crm_sync.py in the background
    try:
        # Get path to current python
        import sys
        python_exe = sys.executable
        script_path = os.path.join(os.getcwd(), "backend", "crm_sync.py")
        
        # We start it as a background process
        subprocess.Popen([python_exe, script_path])
        return {"status": "Sync started in background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
