import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
from confluent_kafka import Producer
import os
import logging

kafka_host = os.getenv('KAFKA_HOST')
kafka_port = os.getenv('KAFKA_PORT')
BASE_URL = "https://asiatimes.com/"


def fetch_articles(soup):
    articles_dict = []
    divs = soup.find_all("div", class_="wp-block-column", limit=6)     
    for div in divs:
        if div.find("div", class_="wp-block-group") is not None: continue 
        if div.find("div", class_="opinion-group") is not None: continue 
        articles = div.find_all("article", limit=20) 
        for article in articles:        
            try:
                title = ""
                if article.find("h2", class_="entry-title") is None:                
                    title = article.find("h3", class_="entry-title").get_text(strip=True)
                    if title is None:
                        continue
                else:
                    title = article.find("h2", class_="entry-title").get_text(strip=True)

                updated_title = title.replace("â€™", "’")
                category = article.find("div", class_="cat-links").get_text(strip=True) if article.find("div", class_="cat-links") else "NA"
                image = article.find("img")["src"] if article.find("img") else "NA"
                link = article.find("a")["href"] if article.find("a") else "NA"      
                articles_dict.append({
                    "Title": updated_title,
                    "Category": category,
                    "Image": image,
                    "Link": link,
                    "Date": datetime.now().strftime("%Y-%m-%d")
                })
            except Exception as e:
                print(f"Error parsing article: {e}")

    return articles_dict

if __name__ == "__main__":
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(BASE_URL, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        if soup:
            article_list = fetch_articles(soup)
            logging.info(f"Articles found: {len(article_list)}")
            print("Articles found:", len(article_list))
            try:
                kafka_producer = Producer({'bootstrap.servers': 'kafka:9093'})
                kafka_producer.produce('asiantimes', json.dumps(article_list))
                
                print(kafka_producer)
        
                kafka_producer.flush()
            except Exception as e:
                print(e)

            # df = pd.DataFrame(articles)
            # df.to_csv("articles.csv", index=False, encoding="utf-8")
                
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}")
            
    

