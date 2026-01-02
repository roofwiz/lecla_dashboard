from fastapi import APIRouter, HTTPException
from backend.app.config import settings
from backend.app.services.jobnimbus import jn_client
from datetime import datetime
import logging
import re

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
async def get_sales_by_rep(year: int = 2025):
    try:
        if not year: year = 2025
        
        # 1. Fetch Data
        jobs = await jn_client.fetch_all_jobs(year_filter=year)
        logger.info(f"Total Jobs Fetched: {len(jobs)}")
        
        if not jobs:
            return {"results": [], "total_revenue": 0, "count": 0, "year": year, "goal": 0}
            
        # 2. Filter & Aggregate
        company_goal = COMPANY_GOALS.get(year, 10000000)
        stats = {}
        total_revenue = 0.0
        total_leads = 0
        total_closed = 0
        valid_rows = 0
        
        start_ts = datetime(year, 1, 1).timestamp()
        end_ts = datetime(year + 1, 1, 1).timestamp()
        
        for job in jobs:
            created_ts = job.get('date_created', 0)
            
            if not (start_ts <= created_ts < end_ts):
                continue
                
            total_leads += 1
            
            status = job.get('status_name', '') or ''
            sales_rep = job.get('sales_rep_name', 'Unknown')
            
            budget = job.get('last_budget_revenue', 0)
            inv = job.get('approved_invoice_total', 0)
            est = job.get('last_estimate', 0)
            
            def safe_float(x):
                try: return float(x)
                except: return 0.0
                
            revenue = max(safe_float(budget), safe_float(inv), safe_float(est))
            
            is_sale_status = any(s.lower() in status.lower() for s in SALES_STATUSES)
            
            if is_sale_status and revenue > 0:
                if sales_rep not in stats: stats[sales_rep] = 0.0
                stats[sales_rep] += revenue
                total_revenue += revenue
                valid_rows += 1
                
            is_closed = any(s.lower() in status.lower() for s in CLOSED_STATUSES)
            if is_closed:
                total_closed += 1
                
        sorted_stats = []
        for rep, total in stats.items():
            if rep:
                sorted_stats.append({"name": rep, "value": total})
                
        sorted_stats.sort(key=lambda x: x['value'], reverse=True)
        
        return {
            "year": year,
            "goal": company_goal,
            "total_revenue": total_revenue,
            "total_leads": total_leads,
            "total_closed": total_closed,
            "results": sorted_stats,
            "count": valid_rows
        }

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
