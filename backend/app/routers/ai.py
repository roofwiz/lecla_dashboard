from fastapi import APIRouter, HTTPException, Depends
import httpx
import logging
from pydantic import BaseModel
from backend.app.config import settings
from backend.app.db import get_db
from backend.app.routers.auth import get_current_user

logger = logging.getLogger(__name__)
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize Vertex AI SDK
try:
    if settings.GCP_SERVICE_ACCOUNT_JSON.exists():
        creds = service_account.Credentials.from_service_account_file(str(settings.GCP_SERVICE_ACCOUNT_JSON))
        vertexai.init(
            project=settings.GCP_PROJECT_ID,
            location=settings.GCP_LOCATION,
            credentials=creds
        )
        logger.info(f"Vertex AI initialized with Service Account for project {settings.GCP_PROJECT_ID}")
    else:
        # Fallback to default auth (works in Cloud Run environments)
        vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_LOCATION)
        logger.info(f"Vertex AI initialized with default auth for project {settings.GCP_PROJECT_ID}")
except Exception as e:
    logger.error(f"Failed to initialize Vertex AI SDK: {e}")

class ChatRequest(BaseModel):
    message: str

PERSONAS = {
    "admin": "You are the Lecla Executive Assistant. You have full access to business metrics and are here to help the owner make strategic decisions.",
    "sales": "You are a Sales Coach for the Lecla team. Your goal is to help reps close more deals and track their leads effectively.",
    "team": "You are a helpful coordinator for the Lecla operations team."
}

from backend.app.database import SessionLocal
from backend.app.models import Job, Budget
from sqlalchemy import func

async def get_business_context():
    """Fetch high-level metrics for AI context infusion."""
    db = SessionLocal()
    try:
        # Active Jobs count
        job_count = db.query(func.count(Job.lecla_id)).scalar() or 0
        
        # Total Revenue (sum of budgets)
        total_rev = db.query(func.sum(Budget.revenue)).scalar() or 0
        
        # Sales Rep performance (top 3)
        top_reps = db.query(
            Budget.sales_rep, 
            func.sum(Budget.revenue).label('rev')
        ).group_by(Budget.sales_rep).order_by(func.sum(Budget.revenue).desc()).limit(3).all()
        
        reps_str = ", ".join([f"{r.sales_rep} (${r.rev:,.0f})" for r in top_reps])
        
        return f"""
        BUSINESS CONTEXT:
        - Active Jobs: {job_count}
        - Total Budgeted Revenue: ${total_rev:,.2f}
        - Top Sales Reps: {reps_str}
        """
    except Exception as e:
        logger.error(f"Error fetching business context: {e}")
        return ""
    finally:
        db.close()

@router.post("/chat")
async def chat_with_agent(req: ChatRequest, current_user: dict = Depends(get_current_user)):
    role = current_user.get("role", "team").lower()
    system_instruction = PERSONAS.get(role, "You are a helpful assistant for Lecla team members.")
    
    # Infuse context
    business_context = await get_business_context()
    
    prompt = f"System Instruction: {system_instruction}\n\n{business_context}\n\nUser Profile: {current_user.get('full_name')} ({role})\n\nUser Message: {req.message}"
    
    try:
        # Use Vertex AI SDK
        model = GenerativeModel("gemini-2.0-flash-exp")
        
        # We run this in a threadpool to avoid blocking the event loop if the SDK is synchronous
        # although vertexai usually handles its own async if used correctly.
        # For simplicity in this dashboard, we'll use the basic call.
        response = model.generate_content(prompt)
        
        if response and response.text:
            return {"response": response.text}
        else:
            return {"response": "The AI returned an empty response."}
                
    except Exception as e:
        logger.error(f"Vertex AI SDK Exception: {e}")
        # Check for specific permission errors to help the user
        if "permission" in str(e).lower():
            return {"response": "I'm having trouble connecting to Google Cloud (Permission Denied). Please ensure the 'Vertex AI User' role is granted."}
        return {"response": f"I'm sorry, I encountered an error: {str(e)[:100]}"}
