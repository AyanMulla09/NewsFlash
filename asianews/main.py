import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
from confluent_kafka import Producer
import os
import logging

kafka_url = os.getenv('KAFKA_URL_INSIDE')
BASE_URL = "https://asianews.network/"


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
            articles_dict.append({
                "Title": title,
                "Category": category,
                "Image": img_link,
                "Link": link,
                "Date": datetime.now().strftime("%Y-%m-%d")
            })

    return articles_dict

if __name__ == "__main__":
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(BASE_URL, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        if soup:
            article_list = fetch_articles(soup)
            try:
                kafka_producer = Producer({'bootstrap.servers': 'kafka:9093'})
                kafka_producer.produce('asianews', json.dumps(article_list))                
        
                kafka_producer.flush()
            except Exception as e:
                print(e)
                
    else:
        print(f"Failed to Fetch asiantimes")
            
    

