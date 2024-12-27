import os
import requests
import json
from confluent_kafka import Producer
import logging
from datetime import datetime
import re

API_KEY = os.getenv('GUARDIAN_API_KEY')
kafka_url = os.getenv('KAFKA_URL_INSIDE')
# API_KEY = '7c194277-c534-4402-9e3f-de51de1ad433'

def fetch_articles():
    today = datetime.now().date().strftime("%Y-%m-%d")
    response = requests.get(f'https://content.guardianapis.com/search?page-size=20&show-fields=thumbnail&q=top&from-date={today}&api-key={API_KEY}')
    response_dict = response.json()
    transformed_results = []
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

    return transformed_results

def report(err, message):
    if err is not None:
        print("Error producing message:", err)

    else:
        print("Message to topic: ", message.topic())  

if __name__ == "__main__":
    try:
        article_list = fetch_articles()
        if article_list :
            kafka_producer = Producer({'bootstrap.servers': kafka_url, 'acks':'all'})
            kafka_producer.produce('guardian', json.dumps(article_list))      
            kafka_producer.flush()

    except Exception as e:
        print(e)



        
