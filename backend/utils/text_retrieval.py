# backend/utils/text_retrieval.py

import requests
from bs4 import BeautifulSoup

def retrieve_post_text(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve URL: {url}")
            return ""
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text from the webpage
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error retrieving URL: {e}")
        return ""
