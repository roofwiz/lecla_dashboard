import os
from dotenv import load_dotenv

load_dotenv('backend/.env')
for key in os.environ:
    if any(x in key for x in ['CAM', 'VERTEX', 'GOOGLE', 'NIMBUS', 'API', 'KEY']):
        print(f"KEY_FOUND: {key}")
