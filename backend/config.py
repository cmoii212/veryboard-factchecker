import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Custom Search API Credentials
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('GOOGLE_CSE_ID')
