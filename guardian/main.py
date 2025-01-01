import os
import requests
import json
from confluent_kafka import Producer
import logging
from datetime import datetime
import re
import redis
import time
import json

API_KEY = os.getenv('GUARDIAN_API_KEY')
kafka_url = os.getenv('KAFKA_URL_INSIDE')
try:
    redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
except redis.ConnectionError as e:
    print(e)
    redis_client = None  

def fetch_articles():
    transformed_results = []
    try :
        today = datetime.now().date().strftime("%Y-%m-%d")
        response = requests.get(f'https://content.guardianapis.com/search?page-size=20&show-fields=thumbnail&q=top&from-date={today}&api-key={API_KEY}')
        response_dict = response.json()        
        for article in response_dict['response']['results']:
            category = article.get("sectionName")
            category = category.replace(" ", "_")
            category = re.sub(r'[^A-Za-z_]', "", category).lower()  
            category = re.sub(r"_+", "_", category)         
            transformed_results.append({
                "Title": article.get("webTitle"),
                "Category": category,
                "Link": article.get("webUrl"),
                "Image": article.get("fields", {}).get("thumbnail"),
                "Date": article.get("webPublicationDate")[:10]
                
            })        

    except Exception as e:
        print(e)
    
    return transformed_results

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
        try:
            article_list = fetch_articles()


            if redis_client:
                    article_list = check_duplicate(article_list)

            if article_list :              
                    
                kafka_producer = Producer({'bootstrap.servers': "kafka:9093", 'acks':'all'})
                
                kafka_producer.produce('guardian', json.dumps(article_list), callback=report)    
                 
                kafka_producer.flush()

        except Exception as e:
            print(e)

        time.sleep(60)


        
