import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from confluent_kafka import Producer
import os
import time
import re
import redis

kafka_url = os.getenv('KAFKA_URL_INSIDE')
BASE_URL = "https://asianews.network/"
try:
    redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)
except redis.ConnectionError as e:
    print(e)
    redis_client = None  

def fetch_articles(soup):
    articles_dict = []
    uls = soup.find_all('ul', class_='newsplus', limit=2)
    for ul in uls:
        li = ul.find_all('li', itemprop='blogPost')
        for article in li:
            title = article.find('h2', class_='entry-title').text.strip() if article.find('h2') else "NA"
            img_tag = article.find('img')
            img_link = img_tag['data-src'] if img_tag else "NA"
            link = article.find('a')['href'] if article.find('a') else "NA"
            
            category_ul = article.find('ul', class_='post-categories')  if article.find('ul', class_='post-categories') else "NA"
            category = category_ul.find("a").text.strip() if category_ul else "NA"
            category = category.replace(" ", "_")
            category = re.sub(r'[^A-Za-z_]', "", category).lower()
            category = re.sub(r"_+", "_", category)
            articles_dict.append({
                "Title": title,
                "Category": category,
                "Image": img_link,
                "Link": link,
                "Date": datetime.now().strftime("%Y-%m-%d")
            })

    return articles_dict

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
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(BASE_URL, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            if soup:
                article_list = fetch_articles(soup)
                if redis_client:
                    article_list = check_duplicate(article_list)
                try:
                    kafka_producer = Producer({'bootstrap.servers': "kafka:9093", 'acks':'all'})
                    kafka_producer.produce('asianews', json.dumps(article_list), callback=report)                
            
                    kafka_producer.flush()
                except Exception as e:
                    print(e)
                    
        else:
            print(f"Failed to Fetch asianews")

        time.sleep(300)
            
    

