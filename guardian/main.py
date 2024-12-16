import os
import requests
import json
from confluent_kafka import Producer

API_KEY = os.getenv('GUARDIAN_API_KEY')
API_KEY = '7c194277-c534-4402-9e3f-de51de1ad433'

def fetch_articles():
    response = requests.get(f'https://content.guardianapis.com/search?page-size=20&show-fields=thumbnail&q=top&api-key={API_KEY}')

    transformed_results = []
    for article in response_dict['response']['results']:
        transformed_results.append({
            "Title": article.get("webTitle"),
            "Category": article.get("sectionName"),
            "Link": article.get("webUrl"),
            "thumbnail": article.get("fields", {}).get("thumbnail"),
            "Date": article.get("webPublicationDate")
            
        })
    
    return transformed_results


if __name__ == "__main__":
    try:
        article_list = fetch_articles()
        kafka_producer = Producer({'bootstrap.servers': 'kafka:9093'})
        kafka_producer.produce('guardian', json.dumps(article_list))
        print(kafka_producer)
        kafka_producer.flush()
    except Exception as e:
        print(e)



        
