import requests
import json
from datetime import datetime
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
import os
import logging
import re
import time
import redis

# Kafka setup
kafka_url = os.getenv('KAFKA_URL_INSIDE')
kafka_topics = ['nyt_articles']

# API setup
NYT_API_KEY = os.getenv('NYT_API_KEY')
NYT_BASE_URL = "https://api.nytimes.com/svc/topstories/v2/{}.json"

try:
    redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
except redis.ConnectionError as e:
    print(e)
    redis_client = None  

def fetch_nyt_articles(section="home"):
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
                section = section.replace(" ", "_")
                section = re.sub(r'[^A-Za-z]', "", section).lower()
                section = re.sub(r"_+", "_", section)
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

def report(err, message):
    if err is not None:
        print("Error producing message:", err)
    else:
        print("Message produced:", message.topic(), message.partition(), message.offset())

def check_duplicate(article_list):
    new_articles = []
    for article_dict in article_list :
        cache_key = article_dict["Title"]
        if not redis_client.exists(cache_key):        
            redis_client.setex(cache_key, 86400, 1)
            new_articles.append(article_dict)
  
    return new_articles

if __name__ == "__main__":
    while True:
        nyt_articles = fetch_nyt_articles("home")
        if redis_client:
                nyt_articles = check_duplicate(nyt_articles)        

        if nyt_articles:
            try:
                kafka_producer = Producer({'bootstrap.servers': "kafka:9093", 'acks':'all'})
                kafka_producer.produce('nyt_articles', json.dumps(nyt_articles), callback=report)                  
                kafka_producer.flush()

            except Exception as e:
                logging.error(f"Error sending NYT articles to Kafka: {e}")
        
        time.sleep(60)        
