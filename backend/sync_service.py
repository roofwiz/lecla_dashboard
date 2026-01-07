import asyncio
import logging
import json
import time
import sys
import os
import httpx

# Add current directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.jobnimbus import jn_client
from app.db import get_db, init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Semaphore for parallel fetching
job_sem = asyncio.Semaphore(15)

async def fetch_job_safe(client, job_id, headers):
    async with job_sem:
        try:
            url = f"{jn_client.base_url}/jobs/{job_id}"
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                return resp.json()
            else:
                return None
        except Exception as e:
            return None

async def sync_jobs_targeted(job_ids):
    logger.info(f"Syncing {len(job_ids)} targeted jobs...")
    
    tasks = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Check existing jobs to avoid re-fetching? 
        # For now, just fetch all needed to ensure freshness as requested.
        
        # We process in chunks of tasks to avoid memory explosion if queueing 100k tasks?
        # But here we probably have ~2000 jobs linked to budgets.
        
        chunk_size = 500
        ids_list = list(job_ids)
        total = len(ids_list)
        
        for i in range(0, total, chunk_size):
            chunk = ids_list[i:i+chunk_size]
            tasks = [fetch_job_safe(client, jid, jn_client.headers) for jid in chunk]
            results = await asyncio.gather(*tasks)
            
            # Save chunk
            with get_db() as conn:
                c = conn.cursor()
                count = 0
                for j in results:
                    if not j: continue
                    jnid = j.get('jnid')
                    number = j.get('number')
                    name = j.get('name')
                    status = j.get('status_name')
                    total_val = j.get('total', 0)
                    date_up = j.get('date_updated', 0)
                    
                    c.execute('''INSERT OR REPLACE INTO jobs 
                                 (jnid, number, name, type, status_name, total, date_updated, data) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                              (jnid, number, name, j.get('type'), status, total_val, date_up, json.dumps(j)))
                    count += 1
                conn.commit()
            logger.info(f"Synced {count} jobs (Chunk {i}-{i+chunk_size})")

async def run_smart_sync():
    init_db()
    
    # 1. Sync Budgets
    logger.info("Step 1: Sync Budgets")
    budgets = await jn_client.fetch_all_budgets() 
    
    with get_db() as conn:
        c = conn.cursor()
        for b in budgets:
            jnid = b.get('jnid')
            number = b.get('number')
            revenue = b.get('revenue', 0)
            sales_rep = b.get('sales_rep_name')
            date_up = b.get('date_updated', 0)
            
            related_job_id = None
            if 'related' in b:
                for rel in b['related']:
                    if rel.get('type') == 'job':
                        related_job_id = rel.get('id')
                        break
            
            c.execute('''INSERT OR REPLACE INTO budgets 
                         (jnid, number, revenue, related_job_id, sales_rep, date_updated, data) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (jnid, number, revenue, related_job_id, sales_rep, date_up, json.dumps(b)))
        conn.commit()
    logger.info(f"Saved {len(budgets)} budgets.")

    # 2. Sync Estimates
    logger.info("Step 2: Sync Estimates")
    estimates = await jn_client.fetch_all_estimates()
    
    with get_db() as conn:
        c = conn.cursor()
        for e in estimates:
            jnid = e.get('jnid')
            number = e.get('number')
            total = e.get('total', 0)
            status = e.get('status_name')
            date_up = e.get('date_updated', 0)
            
            related_job_id = None
            if 'related' in e:
                for rel in e['related']:
                    if rel.get('type') == 'job':
                        related_job_id = rel.get('id')
                        break
            
            c.execute('''INSERT OR REPLACE INTO estimates 
                         (jnid, number, total, related_job_id, status_name, date_updated, data) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (jnid, number, total, related_job_id, status, date_up, json.dumps(e)))
        conn.commit()
    logger.info(f"Saved {len(estimates)} estimates.")

    # 3. Sync Invoices
    logger.info("Step 3: Sync Invoices")
    invoices = await jn_client.fetch_all_invoices()

    with get_db() as conn:
        c = conn.cursor()
        for i in invoices:
            jnid = i.get('jnid')
            number = i.get('number')
            total = i.get('total', 0)
            status = i.get('status_name')
            date_up = i.get('date_updated', 0)
            date_created = i.get('date_created', 0)
            
            # Calculate fees
            fees = 0
            if 'items' in i:
                for item in i['items']:
                    name = item.get('name', '').lower()
                    if 'fee' in name or 'permit' in name or 'surcharge' in name or 'financing' in name:
                        fees += item.get('amount', 0)
            
            related_job_id = None
            if 'related' in i:
                for rel in i['related']:
                    if rel.get('type') == 'job':
                        related_job_id = rel.get('id')
                        break
            
            c.execute('''INSERT OR REPLACE INTO invoices 
                         (jnid, number, total, fees, related_job_id, status_name, date_created, date_updated, data) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (jnid, number, total, fees, related_job_id, status, date_created, date_up, json.dumps(i)))
        conn.commit()
    logger.info(f"Saved {len(invoices)} invoices.")

    # 4. Identify Jobs needed
    needed_job_ids = set()
    for b in budgets:
        if 'related' in b:
            for rel in b['related']:
                if rel.get('type') == 'job':
                    needed_job_ids.add(rel.get('id'))
    
    for e in estimates:
        if 'related' in e:
             for rel in e['related']:
                if rel.get('type') == 'job':
                    needed_job_ids.add(rel.get('id'))
                    
    for i in invoices:
        if 'related' in i:
             for rel in i['related']:
                if rel.get('type') == 'job':
                    needed_job_ids.add(rel.get('id'))

    # 5. Calculate better Job Totals from related data
    logger.info("Step 5: Updating Job Totals from Budgets/Invoices/Estimates")
    with get_db() as conn:
        c = conn.cursor()
        # Update jobs where total is 0 or low, using the max of related financials
        # We join with budgets, estimates, and invoices to find the best representative total
        update_query = """
        UPDATE jobs
        SET total = (
            SELECT MAX(val) FROM (
                SELECT revenue as val FROM budgets WHERE related_job_id = jobs.jnid
                UNION ALL
                SELECT total as val FROM estimates WHERE related_job_id = jobs.jnid
                UNION ALL
                SELECT total as val FROM invoices WHERE related_job_id = jobs.jnid
                UNION ALL
                SELECT total as val FROM (SELECT total FROM jobs j2 WHERE j2.jnid = jobs.jnid)
            )
        )
        WHERE total IS NULL OR total <= 0
        """
        c.execute(update_query)
        affected = c.rowcount
        conn.commit()
    logger.info(f"Updated totals for {affected} jobs.")

    # 6. Sync Targeted Jobs
    if needed_job_ids:
        await sync_jobs_targeted(needed_job_ids)
    else:
        logger.info("No related jobs found to sync.")

if __name__ == "__main__":
    asyncio.run(run_smart_sync())
