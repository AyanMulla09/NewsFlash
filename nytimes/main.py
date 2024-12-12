import requests
import json
from datetime import datetime
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
import os
import logging

# Kafka setup
kafka_url = os.getenv('KAFKA_URL_INSIDE')
kafka_topics = ['nyt_articles']

# API setup
NYT_API_KEY = os.getenv('NYT_API_KEY')
NYT_BASE_URL = "https://api.nytimes.com/svc/topstories/v2/{}.json"

def fetch_nyt_articles(section="home"):
    """Fetch articles from the New York Times Top Stories API for a specific section."""
    try:
        url = NYT_BASE_URL.format(section)
        params = {"api-key": NYT_API_KEY}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("results", [])

            articles_dict = []
            for article in articles:
                title = article.get("title", "NA")
                section = article.get("section", "NA")
                url = article.get("url", "NA")
                published_date = article.get("published_date", "NA")
                
                multimedia = article.get("multimedia", [])
                image_url = multimedia[0]["url"] if multimedia else "NA"

                articles_dict.append({
                    "Title": title,
                    "Category": section,
                    "Image": image_url,
                    "Link": url,
                    "Date": published_date
                })

            return articles_dict
        else:
            logging.error(f"Failed to fetch articles. Status code: {response.status_code}")
            return []

    except Exception as e:
        logging.error(f"Error fetching NYT articles: {e}")
        return []

if __name__ == "__main__":
    # Fetch and produce articles for NYT Top Stories (e.g., "home" section)
    nyt_articles = fetch_nyt_articles("home")
    if nyt_articles:
        try:
            kafka_producer = Producer({'bootstrap.servers': kafka_url})
            kafka_producer.produce('nyt_articles', json.dumps(nyt_articles))
            kafka_producer.flush()
            logging.info("NYT articles successfully sent to Kafka.")
        except Exception as e:
            logging.error(f"Error sending NYT articles to Kafka: {e}")
