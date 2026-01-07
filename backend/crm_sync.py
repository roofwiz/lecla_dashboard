import asyncio
import logging
import json
import uuid
from datetime import datetime
import httpx
from backend.app.services.jobnimbus import jn_client
from backend.app.database import SessionLocal, engine
from backend.app.models import Contact, Job, Base
from backend.app.services.jobnimbus import jn_client

# Create tables if not exists
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_lecla_id(prefix="L"):
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"

async def sync_contacts():
    logger.info("Syncing JobNimbus Contacts to Lecla CRM...")
    contacts = await jn_client.fetch_all_contacts()
    
    db = SessionLocal()
    try:
        count = 0
        for i, jn_contact in enumerate(contacts):
            jn_id = jn_contact.get('jnid')
            
            # Use SQLAlchemy to find existing or create new
            contact = db.query(Contact).filter(Contact.jn_contact_id == jn_id).first()
            
            if not contact:
                contact = Contact(lecla_id=generate_lecla_id("C"), jn_contact_id=jn_id)
                db.add(contact)
            
            contact.first_name = jn_contact.get('first_name', '')
            contact.last_name = jn_contact.get('last_name', '')
            contact.email = jn_contact.get('email', '')
            contact.phone = jn_contact.get('mobile_phone') or jn_contact.get('home_phone') or jn_contact.get('work_phone', '')
            
            contact.address = jn_contact.get('address_line1', '')
            contact.city = jn_contact.get('city', '')
            contact.state = jn_contact.get('state_text', '')
            contact.zip = jn_contact.get('zip', '')
            
            now = int(datetime.now().timestamp())
            contact.date_created = jn_contact.get('date_created', now)
            contact.date_updated = now
            contact.data = jn_contact # JSON column handles dict automatically in SQLAlchemy
            
            count += 1
            if count % 100 == 0:
                db.commit()
                logger.info(f"Committed {count} contacts...")
        db.commit()
        logger.info(f"Synced {count} contacts.")
    finally:
        db.close()

async def sync_jobs():
    logger.info("Syncing JobNimbus Jobs to Lecla CRM...")
    jobs = await jn_client.fetch_all_jobs()
    
    db = SessionLocal()
    try:
        count = 0
        for i, jn_job in enumerate(jobs):
            jn_id = jn_job.get('jnid')
            
            job = db.query(Job).filter(Job.jnid == jn_id).first()
            if not job:
                job = Job(lecla_id=generate_lecla_id("J"), jnid=jn_id)
                db.add(job)
            
            # Find related contact
            contact_lecla_id = None
            if 'related' in jn_job:
                for rel in jn_job['related']:
                    if rel.get('type') == 'contact':
                        rel_contact = db.query(Contact).filter(Contact.jn_contact_id == rel.get('id')).first()
                        if rel_contact:
                            contact_lecla_id = rel_contact.lecla_id
                            break
            
            now = int(datetime.now().timestamp())
            job.number = jn_job.get('number')
            job.name = jn_job.get('name')
            job.type = jn_job.get('type')
            job.status_name = jn_job.get('status_name')
            job.total = jn_job.get('total', 0)
            job.contact_id = contact_lecla_id
            job.date_created = jn_job.get('date_created', now)
            job.date_updated = now
            job.data = jn_job
            
            count += 1
            if count % 100 == 0:
                db.commit()
                logger.info(f"Committed {count} jobs...")
        db.commit()
        logger.info(f"Synced {count} jobs.")
    finally:
        db.close()

async def full_sync():
    await sync_contacts()
    await sync_jobs()
    logger.info("Full CRM Sync completed.")

if __name__ == "__main__":
    asyncio.run(full_sync())
