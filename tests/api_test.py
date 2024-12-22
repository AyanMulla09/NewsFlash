import requests
import json

news_sources = ["nytimes", "guardian", "asianews"]
BASE_URL = "http://localhost:8000/"
def test_api_endpoints():
    for news_source in news_sources:
        response = requests.get(BASE_URL + news_source+"/today")
        assert response.status_code == 200, f"Failed to fetch {news_source}, status code: {response.status_code}"
        assert response.json() is not None, f"Failed to fetch {news_source}, empty response"

        response = requests.get(BASE_URL + news_source+"/categories")
        assert response.status_code == 200, f"Failed to fetch {news_source}, status code: {response.status_code}"
        assert response.json() is not None, f"Failed to fetch {news_source}, empty response"
        assert response.json()["categories"] is not None, f"Failed to fetch {news_source}, empty response"
        response = response.json()
        category = response["categories"]
        category = category[0]

        response = requests.get(BASE_URL + news_source+"/today"+"/"+category)
        assert response.status_code == 200, f"Failed to fetch {news_source}, status code: {response.status_code}"
        assert response.json() is not None, f"Failed to fetch {news_source}, empty response"        
