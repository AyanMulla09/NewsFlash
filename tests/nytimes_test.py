import requests
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nytimes.main import fetch_nyt_articles

NYT_BASE_URL = "https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json"
NYT_API_KEY = os.getenv('NYT_API_KEY')

def test_fetch_nyt_articles():
    # Test the API response directly
    params = {"api-key": NYT_API_KEY}
    response = requests.get(NYT_BASE_URL, params=params)
    assert response.status_code == 200, f"Failed to fetch NYT articles, status code: {response.status_code}"
    assert response.json() is not None, "Failed to fetch NYT articles, empty response"
    
    # Test the fetch_nyt_articles function
    articles = fetch_nyt_articles()
    assert isinstance(articles, list), "fetch_nyt_articles did not return a list"
    assert len(articles) > 0, "No articles fetched by fetch_nyt_articles"
    for article in articles:
        assert "Title" in article, "Missing 'Title' in an article"
        assert "Category" in article, "Missing 'Category' in an article"
        assert "Link" in article, "Missing 'Link' in an article"
        assert "Date" in article, "Missing 'Date' in an article"
        assert "Image" in article, "Missing 'Image' in an article"

if __name__ == "__main__":
    test_fetch_nyt_articles()
    print("All tests passed!")
