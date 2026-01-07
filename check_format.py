import os
from dotenv import load_dotenv
load_dotenv('backend/.env')

def check_token(name):
    val = os.getenv(name)
    if not val:
        print(f"{name}: NOT FOUND")
        return
    print(f"{name}: Length={len(val)}, Start='{val[:2]}', End='{val[-2:]}', Spaces='{val != val.strip()}'")

check_token('COMPANY_CAM_TOKEN')
check_token('VERTEX_AI_API_KEY')
check_token('GOOGLE_MAPS_PLATFORM_API_KEY')
