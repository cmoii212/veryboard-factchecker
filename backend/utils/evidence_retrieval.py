import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from utils.text_retrieval import retrieve_post_text

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')

def retrieve_evidence(claim):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    res = service.cse().list(q=claim, cx=GOOGLE_CSE_ID, num=5).execute()
    evidence_list = []
    if 'items' in res:
        for item in res['items']:
            url = item['link']
            content = retrieve_post_text(url)
            evidence_list.append({'url': url, 'content': content})
    return evidence_list
