from fastapi import APIRouter, HTTPException
from backend.app.config import settings
from backend.app.services.jobnimbus import jn_client
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
async def get_sales_by_rep(year: int = 2025):
    """
    Generate Sales Report from JobNimbus Data (Safe & Optimized).
    """
    try:
        if not year: 
            year = datetime.now().year
        
        company_goal = COMPANY_GOALS.get(year, 10000000)
        stats = {}
        total_revenue = 0.0
        total_leads = 0
        total_closed = 0
        valid_rows = 0
        
        # Unix Timestamps for Year filtering
        start_ts = datetime(year, 1, 1).timestamp()
        end_ts = datetime(year + 1, 1, 1).timestamp()
        
        limit = 1000
        skip = 0
        stop_fetching = False
        last_first_id = None
        
        logger.info(f"Generating safe report for year {year}")

        while not stop_fetching:
            logger.info(f"Fetching JN Jobs: skip={skip}")
            jobs_page = await jn_client.get_jobs_simple(limit=limit, skip=skip)
            
            if not jobs_page:
                break
                
            # DUPLICATE DETECTION:
            # JobNimbus API V1 often ignores 'skip/offset' on the /jobs endpoint.
            # If we see the same first result twice, we are stuck in an infinite loop.
            current_first_id = jobs_page[0].get('jnid')
            if last_first_id and current_first_id == last_first_id:
                logger.warning(f"Detected duplicate results at skip {skip}. API likely does not support paging. Stopping.")
                break
            last_first_id = current_first_id
            
            page_in_range = False
            for job in jobs_page:
                created_ts = job.get('date_created', 0)
                
                # Check if within range
                if start_ts <= created_ts < end_ts:
                    page_in_range = True
                    total_leads += 1
                    status = job.get('status_name', '') or ''
                    sales_rep = job.get('sales_rep_name', 'Unknown')
                    
                    budget = job.get('last_budget_revenue', 0)
                    inv = job.get('approved_invoice_total', 0)
                    est = job.get('last_estimate', 0)
                    
                    def safe_float(x):
                        try:
                            if x is None: return 0.0
                            return float(x)
                        except:
                            return 0.0
                            
                    revenue = max(safe_float(budget), safe_float(inv), safe_float(est))
                    
                    # Sale check
                    is_sale_status = any(s.lower() in status.lower() for s in SALES_STATUSES)
                    if is_sale_status and revenue > 0:
                        if sales_rep not in stats: stats[sales_rep] = 0.0
                        stats[sales_rep] += revenue
                        total_revenue += revenue
                        valid_rows += 1
                        
                    # Closed check
                    is_closed = any(s.lower() in status.lower() for s in CLOSED_STATUSES)
                    if is_closed:
                        total_closed += 1
                elif created_ts < start_ts:
                    # If we find a job OLDER than our start point, and assuming DESC order, we can stop.
                    # But only if we were actually IN the range already or if first job of the account is older.
                    if skip > 0 or len(jobs_page) < limit:
                        # Optimization: we hit the end of the year's data
                        pass
            
            # Since pagination might be broken, we'll only try once if we don't have a working filter.
            # But we increment skip anyway in case it DOES work.
            skip += len(jobs_page)
            if len(jobs_page) < limit:
                stop_fetching = True
            
            # Absolute limit to prevent server hung/timeout in case of weirdness
            if skip > 5000: break

        # Format results
        sorted_stats = [{"name": rep, "value": total} for rep, total in stats.items() if rep]
        sorted_stats.sort(key=lambda x: x['value'], reverse=True)
        
        return {
            "year": year,
            "goal": company_goal,
            "total_revenue": total_revenue,
            "total_leads": total_leads,
            "total_closed": total_closed,
            "results": sorted_stats,
            "count": valid_rows,
            "note": "Data limited by API pagination constraints" if skip >= 1000 and last_first_id else None
        }

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
