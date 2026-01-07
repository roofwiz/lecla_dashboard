"""
JobNimbus Bidirectional Sync Module

Provides functions for:
1. Syncing jobs FROM JobNimbus to local DB (with full custom field mapping)
2. Pushing updates TO JobNimbus when fields are changed locally
"""

import aiohttp
from backend.app.config import settings
from backend.app.models import Job
from backend.app.database import SessionLocal
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class JobNimbusSync:
    """Handle bidirectional sync with JobNimbus"""
    
    def __init__(self):
        self.api_base = "https://app.jobnimbus.com/api1"
        self.headers = {
            "Authorization": f"Bearer {settings.JOB_NIMBUS_API_TOKEN}",
            "Content-Type": "application/json"
        }
    
    async def fetch_job_details(self, jnid: str):
        """Fetch full job details from JobNimbus API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_base}/jobs/{jnid}",
                headers=self.headers
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    logger.error(f"Failed to fetch job {jnid}: {resp.status}")
                    return None
    
    async def update_job_field(self, jnid: str, field_name: str, value):
        """
        Update a single field in JobNimbus
        
        Args:
            jnid: JobNimbus job ID
            field_name: Field key (e.g., 'TotalProject', 'FileDate')
            value: New value for the field
        """
        # Prepare payload
        payload = {field_name: value}
        
        # Convert dates to MM/DD/YYYY if needed
        if isinstance(value, int) and field_name.endswith('Date'):
            date_obj = datetime.fromtimestamp(value)
            payload[field_name] = date_obj.strftime('%m/%d/%Y')
        
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.api_base}/jobs/{jnid}",
                headers=self.headers,
                json=payload
            ) as resp:
                if resp.status in [200, 204]:
                    logger.info(f"Updated job {jnid} field {field_name} = {value}")
                    return True
                else:
                    logger.error(f"Failed to update job {jnid}: {resp.status}")
                    error_text = await resp.text()
                    logger.error(f"Error details: {error_text}")
                    return False
    
    async def sync_job_to_jobnimbus(self, job: Job):
        """
        Push all changed fields from local Job to JobNimbus
        
        This is called when user updates a job in the dashboard
        """
        payload = {}
        
        # Core fields
        if job.name:
            payload['name'] = job.name
        if job.type:
            payload['type'] = job.type
        if job.service_type:
            payload['ServiceType'] = job.service_type
        if job.status_name:
            payload['status_name'] = job.status_name
        
        # Financial fields
        if job.total_project is not None:
            payload['TotalProject'] = job.total_project
        if job.total_gross is not None:
            payload['TotalGross'] = job.total_gross
        if job.total_net is not None:
            payload['TotalNet'] = job.total_net
        if job.permit_fee is not None:
            payload['PermitFee'] = job.permit_fee
        if job.financing_fee is not None:
            payload['FinancingFee'] = job.financing_fee
        
        # Date fields (convert to MM/DD/YYYY)
        if job.first_estimate_signed_date:
            date_obj = datetime.fromtimestamp(job.first_estimate_signed_date)
            payload['FirstEstimateSignedDate'] = date_obj.strftime('%m/%d/%Y')
        if job.second_estimate_signed_date:
            date_obj = datetime.fromtimestamp(job.second_estimate_signed_date)
            payload['SecondEstimateSignedDate'] = date_obj.strftime('%m/%d/%Y')
        if job.paid_in_full_date:
            date_obj = datetime.fromtimestamp(job.paid_in_full_date)
            payload['PaidInFullDate'] = date_obj.strftime('%m/%d/%Y')
        if job.file_date:
            date_obj = datetime.fromtimestamp(job.file_date)
            payload['FileDate'] = date_obj.strftime('%m/%d/%Y')
        
        # Boolean fields
        if job.is_repeat_customer is not None:
            payload['IsRepeatCustomer'] = bool(job.is_repeat_customer)
        if job.warranty_and_permit_closed is not None:
            payload['WarrantyAndPermitClosed'] = bool(job.warranty_and_permit_closed)
        
        # Contact fields
        if job.sales_rep:
            payload['SalesRep'] = job.sales_rep
        if job.primary_contact:
            payload['PrimaryContact'] = job.primary_contact
        if job.subcontractors:
            # Convert array to comma-separated string if needed
            if isinstance(job.subcontractors, list):
                payload['Subcontractors'] = ', '.join(job.subcontractors)
            else:
                payload['Subcontractors'] = job.subcontractors
        
        # Send update to JobNimbus
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.api_base}/jobs/{job.jnid}",
                headers=self.headers,
                json=payload
            ) as resp:
                if resp.status in [200, 204]:
                    logger.info(f"Successfully synced job {job.jnid} to JobNimbus")
                    return True
                else:
                    logger.error(f"Failed to sync job {job.jnid}: {resp.status}")
                    error_text = await resp.text()
                    logger.error(f"Error details: {error_text}")
                    return False

# Global instance
jn_sync = JobNimbusSync()
