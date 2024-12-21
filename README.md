# COMP41720

## Setup
CLI Commands:
```
git clone https://gitlab.com/Glenmic/COMP41720.git
git checkout develop
git pull origin develop
git checkout feature/frontend
docker-compose up
```

CLI Commands open frontend page
```
git clone https://gitlab.com/Glenmic/COMP41720.git
git checkout combine-project
git pull origin combine-project
docker-compose up
open http://localhost:8080/#/
```

## .env file
Create a .env file in the root folder and paste the below details
```
POSTGRES_DB="news"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="password"
POSTGRES_HOST="database"
POSTGRES_PORT="5432"
KAFKA_ADVERTISED_LISTENERS="INSIDE://kafka:9093,OUTSIDE://localhost:9092"
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP="INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT"
KAFKA_LISTENERS="INSIDE://0.0.0.0:9093,OUTSIDE://0.0.0.0:9092"
KAFKA_INTER_BROKER_LISTENER_NAME="INSIDE"
KAFKA_ZOOKEEPER_CONNECT="zookeeper:2181"
KAFKA_CREATE_TOPICS="asianews:1:1"
KAFKA_URL_INSIDE="kafka:9093"
```


Navigate to http://localhost:8000/

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

