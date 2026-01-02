from app.config import settings
import requests
import json

def scan_revenue():
    token = settings.JOB_NIMBUS_TOKEN
    url = "https://app.jobnimbus.com/api1/jobs?limit=1000"
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🌍 Fetching Jobs...")
    res = requests.get(url, headers=headers)
    items = res.json()
    if isinstance(items, dict) and 'results' in items: items = items['results']
    
    print(f"Got {len(items)} items.")
    
    closed_count = 0
    # Print 5 examples of "Closed" or "Paid" or "Signed"
    print(f"{'Status':<20} | {'BudgetRev':<10} | {'InvTotal':<10} | {'LastEst':<10}")
    print("-" * 60)
    
    for item in items:
        status = item.get('status_name', '')
        # Check pertinent fields
        budget = item.get('last_budget_revenue', 0)
        inv = item.get('approved_invoice_total', 0)
        est = item.get('last_estimate', 0)
        
        # Filter for interesting ones
        if budget > 0 or inv > 0 or "Closed" in status or "Paid" in status or "Signed" in status:
             print(f"{status[:20]:<20} | {budget:<10} | {inv:<10} | {est:<10}")
             closed_count += 1
             if closed_count >= 20: break

scan_revenue()
