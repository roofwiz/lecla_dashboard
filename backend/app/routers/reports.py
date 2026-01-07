from fastapi import APIRouter, HTTPException, Depends
from backend.app.database import get_db as get_sqlalchemy_db
from backend.app.models import Job, Budget
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Constants
COMPANY_GOALS = {
    2024: 8000000,
    2025: 10000000,
    2026: 14000000
}

SALES_STATUSES = [
    'Paid & Closed', 'Signed - pending dep', 'Pending Payments', 
    'Jobs In Progress', 'Job Prep', 'Job Completed', 
    'Insurance Approved', 'Signed Contract', 'Contangency Agreement Signed',
    'Signed - pending deposit'
]
CLOSED_STATUSES = ['Paid & Closed', 'Job Completed']

@router.get("/sales-by-rep")
async def get_sales_by_rep(year: int = 2025, db: Session = Depends(get_sqlalchemy_db)):
    """
    Generate Sales Report from local database (SQLAlchemy).
    Uses estimate signed date to determine which year a sale belongs to.
    """
    try:
        startTime = int(datetime(year, 1, 1).timestamp())
        endTime = int(datetime(year + 1, 1, 1).timestamp())
        company_goal = COMPANY_GOALS.get(year, 10000000)
        
        # Pull budgets for this year (budget date is most accurate for sales)
        budgets = db.query(Budget).filter(
            Budget.date_updated >= startTime, 
            Budget.date_updated < endTime
        ).all()
        
        stats = {}
        total_revenue = 0.0
        
        for budget in budgets:
            # Get sales rep from budget
            rep = budget.sales_rep or "Unknown"
            rev = budget.revenue or 0.0
            stats[rep] = stats.get(rep, 0.0) + rev
            total_revenue += rev
            
        # Pull job stats (based on budget date)
        total_leads = db.query(func.count(Job.lecla_id)).join(
            Budget, Job.jnid == Budget.related_job_id
        ).filter(
            Budget.date_updated >= startTime,
            Budget.date_updated < endTime
        ).scalar() or 0
        
        total_closed = db.query(func.count(Job.lecla_id)).join(
            Budget, Job.jnid == Budget.related_job_id
        ).filter(
            Budget.date_updated >= startTime,
            Budget.date_updated < endTime,
            Job.status_name.in_(CLOSED_STATUSES)
        ).scalar() or 0
        
        # Format results
        sorted_stats = [{"name": rep, "value": round(total, 2)} for rep, total in stats.items() if rep]
        sorted_stats.sort(key=lambda x: x['value'], reverse=True)
        
        return {
            "year": year,
            "goal": company_goal,
            "total_revenue": round(total_revenue, 2),
            "total_leads": total_leads,
            "total_closed": total_closed,
            "results": sorted_stats,
            "count": len(budgets)
        }

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs-by-rep/{rep_name}")
async def get_jobs_by_rep(rep_name: str, year: int = 2025, db: Session = Depends(get_sqlalchemy_db)):
    """
    Get all jobs for a specific sales rep for drill-down from reports.
    """
    try:
        startTime = int(datetime(year, 1, 1).timestamp())
        endTime = int(datetime(year + 1, 1, 1).timestamp())
        
        # Get jobs with budgets for this sales rep
        jobs = db.query(Job).join(
            Budget, Job.jnid == Budget.related_job_id
        ).filter(
            Budget.sales_rep == rep_name,
            Budget.date_updated >= startTime,
            Budget.date_updated < endTime
        ).order_by(Job.date_updated.desc()).all()
        
        # Format for frontend
        return [{
            "jnid": job.jnid,
            "number": job.number,
            "name": job.name,
            "status_name": job.status_name,
            "total": job.total,
            "date_created": job.date_created,
            "sales_rep": rep_name
        } for job in jobs]
        
    except Exception as e:
        logger.error(f"Error fetching jobs for rep {rep_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
