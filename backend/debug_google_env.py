from app.config import settings
import os

print(f"GOOGLE_API_KEY from Settings: '{settings.GOOGLE_API_KEY}'")
if settings.GOOGLE_API_KEY:
    masked = f"{settings.GOOGLE_API_KEY[:4]}...{settings.GOOGLE_API_KEY[-4:]}"
    print(f"Masked: {masked}")
else:
    print("Key is empty")
