from fastapi import APIRouter, HTTPException
from backend.app.routers.google import get_google_creds
from googleapiclient.discovery import build
from datetime import datetime, UTC

router = APIRouter()

@router.get("/events")
def get_events():
    """Fetch upcoming events from the user's primary Google Calendar."""
    creds = get_google_creds()
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        # Call the Calendar API
        now = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=now,
            maxResults=50, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
        
    except Exception as e:
        print(f"Google Calendar Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
