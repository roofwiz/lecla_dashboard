"""
JobNimbus Financial Calculator

Handles the dual-source financial data logic:
- TotalProject: Sum of all invoices
- TotalGross/TotalNet: From active budget
- Commissions: Extracted from budget expenses
"""

import aiohttp
from backend.app.config import settings
import logging

logger = logging.getLogger(__name__)

class JobNimbusFinancialCalculator:
    """Calculate job financials from Invoices and Budgets"""
    
    def __init__(self, api_token: str):
        self.api_base = "https://app.jobnimbus.com/api1"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    async def get_job_invoices(self, job_id: str):
        """
        Fetch all invoices for a job
        Returns only active invoices (excludes Void, Draft)
        """
        async with aiohttp.ClientSession() as session:
            # JobNimbus API: Get related invoices
            async with session.get(
                f"{self.api_base}/jobs/{job_id}/related/invoices",
                headers=self.headers
            ) as resp:
                if resp.status == 200:
                    invoices = await resp.json()
                    # Filter out void/draft invoices
                    active_invoices = [
                        inv for inv in invoices
                        if inv.get('status_name', '').lower() not in ['void', 'draft', 'cancelled']
                    ]
                    return active_invoices
                else:
                    logger.error(f"Failed to fetch invoices for job {job_id}: {resp.status}")
                    return []
    
    async def get_job_budgets(self, job_id: str):
        """
        Fetch budgets for a job
        Returns the active budget (or most recent if multiple exist)
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_base}/jobs/{job_id}/related/budgets",
                headers=self.headers
            ) as resp:
                if resp.status == 200:
                    budgets = await resp.json()
                    if not budgets:
                        return None
                    
                    # Find active budget
                    active_budget = next(
                        (b for b in budgets if b.get('is_active') or b.get('status') == 'Active'),
                        None
                    )
                    
                    # If no active budget, use most recent
                    if not active_budget and budgets:
                        budgets_sorted = sorted(
                            budgets,
                            key=lambda b: b.get('date_modified', 0),
                            reverse=True
                        )
                        active_budget = budgets_sorted[0]
                    
                    return active_budget
                else:
                    logger.error(f"Failed to fetch budgets for job {job_id}: {resp.status}")
                    return None
    
    async def calculate_job_financials(self, job_id: str):
        """
        Calculate all financial fields for a job with correct business logic
        
        CRITICAL: TotalProject (Effective Revenue) = Invoices - Pass-through fees
        
        Execution Order:
        1. GET job to read current PermitFee and FinancingFee (manual entries)
        2. GET invoices and budgets
        3. COMPUTE effective revenue
        4. Return calculated values
        
        Returns dict with:
        - total_invoiced: Raw sum of all invoice totals
        - permit_fee: From job custom field (user-entered)
        - financing_fee: From job custom field (user-entered)
        - total_project: Effective revenue (invoiced - pass-through fees)
        - total_gross: Gross profit from budget
        - total_net: Net profit from budget
        - commissions: Sum of commission line items from budget
        """
        
        # Step 1: GET current job to read permit_fee and financing_fee
        # These are manually entered by users, so we read them first
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_base}/jobs/{job_id}",
                headers=self.headers
            ) as resp:
                if resp.status == 200:
                    job_data = await resp.json()
                else:
                    logger.error(f"Failed to fetch job {job_id}")
                    job_data = {}
        
        # Extract permit fee and financing fee (user-entered values)
        permit_fee = float(job_data.get('permit_fee') or job_data.get('PermitFee') or 0)
        financing_fee = float(job_data.get('financing_fee') or job_data.get('FinancingFee') or 0)
        
        # Step 2: Fetch invoices and budgets in parallel
        invoices, budget = await asyncio.gather(
            self.get_job_invoices(job_id),
            self.get_job_budgets(job_id)
        )
        
        # Step 3: Calculate total invoiced (before subtracting pass-throughs)
        total_invoiced = sum(
            float(inv.get('total', 0) or 0)
            for inv in invoices
        )
        
        # CRITICAL: Calculate Effective Revenue (True Top Line)
        # Formula: Total Invoiced - Permit Fee - Financing Fee
        total_project = total_invoiced - permit_fee - financing_fee
        
        # Extract margins from budget
        total_gross = 0.0
        total_net = 0.0
        commissions = 0.0
        
        if budget:
            # Try different possible field names for gross/net
            total_gross = float(
                budget.get('gross_profit') or 
                budget.get('grossProfit') or 
                budget.get('total_gross') or 
                budget.get('revenue') or 
                0
            )
            
            total_net = float(
                budget.get('net_profit') or 
                budget.get('netProfit') or 
                budget.get('total_net') or 
                budget.get('net_revenue') or 
                0
            )
            
            # Extract commissions from expenses
            expenses = budget.get('expenses', []) or budget.get('line_items', [])
            for expense in expenses:
                description = expense.get('description', '').lower()
                if 'commission' in description:
                    amount = float(expense.get('total', 0) or expense.get('amount', 0) or 0)
                    commissions += amount
        
        return {
            'total_invoiced': total_invoiced,      # Raw invoice sum
            'permit_fee': permit_fee,              # Pass-through cost
            'financing_fee': financing_fee,        # Pass-through cost
            'total_project': total_project,        # EFFECTIVE REVENUE (Top Line)
            'total_gross': total_gross,
            'total_net': total_net,
            'commissions': commissions
        }
    
    async def sync_financials_to_fields(self, job_id: str):
        """
        Calculate financials and push back to JobNimbus custom fields
        
        Follows proper execution order:
        1. READ existing permit_fee and financing_fee (manual entries)
        2. CALCULATE effective revenue
        3. PATCH update to JobNimbus
        
        This is the main orchestration function
        """
        # Calculate values (includes reading current permit/financing fees)
        financials = await self.calculate_job_financials(job_id)
        
        # Prepare update payload (only calculated fields, NOT permit/financing fees)
        # We don't overwrite user-entered permit_fee and financing_fee
        update_payload = {
            'TotalProject': financials['total_project'],        # Effective revenue
            'TotalGross': financials['total_gross'],
            'TotalNet': financials['total_net'],
            'TotalCommissions': financials['commissions'],
            'FileDate': datetime.now().strftime('%m/%d/%Y')     # Timestamp the sync
        }
        
        # Send PATCH update to JobNimbus
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"{self.api_base}/jobs/{job_id}",
                headers=self.headers,
                json=update_payload
            ) as resp:
                if resp.status in [200, 204]:
                    logger.info(f"Successfully synced financials for job {job_id}")
                    logger.info(f"Total Invoiced: ${financials['total_invoiced']:,.2f}")
                    logger.info(f"Permit Fee: ${financials['permit_fee']:,.2f}")
                    logger.info(f"Financing Fee: ${financials['financing_fee']:,.2f}")
                    logger.info(f"→ Effective Revenue (TotalProject): ${financials['total_project']:,.2f}")
                    logger.info(f"TotalGross: ${financials['total_gross']:,.2f}")
                    logger.info(f"TotalNet: ${financials['total_net']:,.2f}")
                    logger.info(f"Commissions: ${financials['commissions']:,.2f}")
                    return True
                else:
                    logger.error(f"Failed to sync financials for job {job_id}: {resp.status}")
                    return False

# Global instance
import asyncio
from datetime import datetime

financial_calc = JobNimbusFinancialCalculator(settings.JOB_NIMBUS_TOKEN)
