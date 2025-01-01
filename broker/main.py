from confluent_kafka import Consumer, KafkaException, KafkaError
from json import loads
import psycopg2
import os
import logging
from psycopg2 import sql
from datetime import datetime, timedelta


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
    try:
        query = "INSERT INTO {table} (title, category, image, link, date) VALUES (%s, %s, %s, %s, %s);"
        sql_query = sql.SQL(query).format(table=sql.Identifier(news_source))
        insert_values = [(row['Title'], row['Category'], row['Image'], row['Link'], row['Date']) for row in data]
        cursor.executemany(sql_query, insert_values)
        conn.commit()
    except Exception as e:
        print(e)

def test_service(news_source):
    print("*"*10+news_source+"*"*10)
    try:
        query = "SELECT * FROM {table};"
        sql_query = sql.SQL(query).format(table=sql.Identifier(news_source))
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)  
                  
    except Exception as e:
        print(e)    


def del_past_data(news_source):
    day_before_yesterday = datetime.today() - timedelta(days=3)
    day_before_yesterday = day_before_yesterday.date().strftime("%Y-%m-%d")
    try:
        query = "DELETE FROM {table} WHERE date < %s;"
        sql_query = sql.SQL(query).format(table=sql.Identifier(news_source))
        cursor.execute(sql_query, (day_before_yesterday,))
        conn.commit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    broker = Consumer({
        'bootstrap.servers': 'kafka:9093',
        'group.id': 'news_services',
        'auto.offset.reset': 'earliest'
    })
    broker.subscribe(['asianews', 'nyt_articles', 'guardian'])

    try:
        while True:          
            data = broker.poll(timeout=1.0)
            if data is None:
                continue
           
            if data.error():
                print(f"Error: {data.error()}")
                continue
           
            message_value = data.value().decode('utf-8')  
            message_data = loads(message_value) 

                            
            topic = data.topic()  
            if topic == 'asianews':
                del_past_data("asianews")                 
                insert_db(message_data, 'asianews')
                
            elif topic == 'nyt_articles':
                del_past_data("nytimes")                
                insert_db(message_data, 'nytimes')                    

            elif topic == 'guardian':
            
                del_past_data("guardian")                
                insert_db(message_data, 'guardian')            


    except Exception as e:
        print(e)
