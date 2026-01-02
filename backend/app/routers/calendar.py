from fastapi import APIRouter

router = APIRouter()

@router.get("/events")
def get_events():
    # Return empty list for now to silence errors
    return []
