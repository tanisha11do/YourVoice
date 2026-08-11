import os
from dotenv import load_dotenv

load_dotenv()

CALLE_API_KEY = os.getenv("CALLE_API_KEY")

if not CALLE_API_KEY:
    raise ValueError("CALLE_API_KEY is not configured")