from fastapi import APIRouter, HTTPException, Depends
from backend.app.database import get_db
from backend.app.models import Job
from backend.app.services.financial_calculator import financial_calc
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class FinancialResponse(BaseModel):
    total_invoiced: float
    permit_fee: float
    financing_fee: float
    total_project: float
    total_gross: float
    total_net: float
    commissions: float

@router.post("/calculate/{job_jnid}", response_model=FinancialResponse)
async def calculate_financials(job_jnid: str, db: Session = Depends(get_db)):
    """
    Calculate financials for a job from JobNimbus invoices and budgets
    
    This performs:
    1. Fetch invoices and sum totals
    2. Fetch budget for margins
    3. Calculate effective revenue (invoiced - pass-through fees)
    4. Extract commissions
    """
    try:
        financials = await financial_calc.calculate_job_financials(job_jnid)
        
        # Also update local DB cache
        job = db.query(Job).filter(Job.jnid == job_jnid).first()
        if job:
            job.total_project = financials['total_project']
            job.total_gross = financials['total_gross']
            job.total_net = financials['total_net']
            job.permit_fee = financials['permit_fee']
            job.financing_fee = financials['financing_fee']
            db.commit()
        
        return financials
    except Exception as e:
        logger.error(f"Failed to calculate financials for {job_jnid}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/job/{job_jnid}", response_model=FinancialResponse)
def get_job_financials(job_jnid: str, db: Session = Depends(get_db)):
    """
    Get cached financial data for a job from local DB
    
    Use /calculate/{job_jnid} to recalculate from JobNimbus
    """
    job = db.query(Job).filter(Job.jnid == job_jnid).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        'total_invoiced': (job.total_project or 0) + (job.permit_fee or 0) + (job.financing_fee or 0),
        'permit_fee': job.permit_fee or 0,
        'financing_fee': job.financing_fee or 0,
        'total_project': job.total_project or 0,
        'total_gross': job.total_gross or 0,
        'total_net': job.total_net or 0,
        'commissions': job.commissions if hasattr(job, 'commissions') else 0
    }

@router.post("/sync/{job_jnid}")
async def sync_financials_to_jobnimbus(job_jnid: str):
    """
    Calculate financials and push back to JobNimbus custom fields
    
    This updates TotalProject, TotalGross, TotalNet, TotalCommissions
    """
    try:
        success = await financial_calc.sync_financials_to_fields(job_jnid)
        if success:
            return {"status": "success", "message": "Financials synced to JobNimbus"}
        else:
            raise HTTPException(status_code=500, detail="Failed to sync to JobNimbus")
    except Exception as e:
        logger.error(f"Failed to sync financials for {job_jnid}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
