from confluent_kafka import Consumer, KafkaException, KafkaError
from json import loads
import psycopg2
import os
import logging
import pandas as pd

db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')
db_name = os.getenv('POSTGRES_DB')
kafka_url = os.getenv('KAFKA_URL_INSIDE')

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)
cursor = conn.cursor()

def insert_db(data, news_source):
    for data_dict in data:
        try:
            query = "INSERT INTO "+news_source+" (title, category, image, link, date) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query, (data_dict['Title'], data_dict['Category'], data_dict['Image'], data_dict['Link'], data_dict['Date']))
            conn.commit()
        except Exception as e:
            print(e)

def test_service(news_source):
    try:
        query = "SELECT * FROM "+news_source+";"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    broker = Consumer({
        'bootstrap.servers': 'kafka:9093',
        'group.id': 'news_services',
        'auto.offset.reset': 'earliest'
    })
    broker.subscribe(['asianews', 'nyt_articles'])  # Subscribe to both topics

    try:
        while True:
            # Poll for messages
            data = broker.poll(timeout=1.0)
            if data is None:
                continue

            # Check if the message has an error
            if data.error():
                print(f"Error: {data.error()}")
                continue

            # Decode the message value and load it as JSON
            message_value = data.value().decode('utf-8')  # Decode the message payload (assuming it's UTF-8)
            message_data = loads(message_value)  # Parse the JSON

            # Extract topic and process data
            topic = data.topic()  # Get the topic from the Kafka message
            if topic == 'asianews':
                insert_db(message_data, "asianews")
                test_service("asianews")
            elif topic == 'nyt_articles':
                insert_db(message_data, "nytimes")
                test_service("nytimes")

    except Exception as e:
        print(e)
