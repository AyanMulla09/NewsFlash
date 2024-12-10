import requests
from bs4 import BeautifulSoup
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from asianews.main import fetch_articles

BASE_URL = "https://asianews.network/"

def test_fetch_articles():
    headers = {"User-Agent": "Mozilla/5.0"}    
    response = requests.get(BASE_URL, headers=headers)    
    response.encoding = 'utf-8'
    assert response.status_code == 200, "Failed to fetch asianews, status code: {}".format(response.status_code) 
    soup = BeautifulSoup(response.content, "html.parser")    
    assert soup is not None, "Failed to parse asiantimes"
    articles = fetch_articles(soup)    
    assert len(articles) > 0, "No articles found"