# NewsFlash - A Distributed News Aggregation System

## Overview

NewsFlash is a distributed system designed to aggregate, process, and display news articles from various sources in real time. The system leverages Docker, Kafka, PostgreSQL, and FastAPI to ensure scalability, fault tolerance, and ease of use. News articles are fetched from multiple sources, processed into a standardized format, and stored in a relational database, making them accessible through a REST API.

---

## Features

- **Distributed Architecture**: Scalable design with clearly defined data collection, processing, and storage layers.
- **Fault Tolerance**: Built-in fault tolerance using Kafka with Zookeeper and PostgreSQL.
- **REST API**: FastAPI provides easy-to-use endpoints for fetching news articles.
- **Dockerized Deployment**: All components are containerized for easy setup and deployment.
- **Category Segregation**: News articles are categorized for efficient querying.

---

## Technology Stack

1. **Docker/Docker Compose**: Containerization for all services.
2. **Apache Kafka**: Message broker for asynchronous data transfer.
3. **PostgreSQL**: Relational database for structured storage of news articles.
4. **FastAPI**: Backend framework for REST API development.
5. **Python**: Data collection and processing scripts.
6. **Redis**: Caching the data fetched from the APIs.

---

## System Architecture

The system is divided into three primary layers:

1. **Data Collection Layer**:
    - Collects raw data from news sources via APIs or web scraping.
    - Processes data into a standardized JSON format.
2. **Data Processing Layer**:
    - Kafka brokers handle data transfer from collection services to the storage layer.
    - Zookeeper ensures fault tolerance for Kafka.
3. **Frontend Layer**:
    - FastAPI provides API endpoints for accessing the stored news data.
    - Frontend clients consume this API to display data to users.

---

## Installation and Setup

### Prerequisites

- Docker and Docker Compose installed on your system.
- Python 3.8 or higher (for development and scripts).

### Steps

1. **Clone the Repository**:
    
    ```bash
    git clone https://gitlab.com/Glenmic/COMP41720.git
    cd COMP41720
    ```
    
2. **Set Up Environment Variables**:
    
    - Create a `.env` file in the root directory with the following variables:
        ```env
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
        KAFKA_CREATE_TOPICS="asianews:1:1,nyt_articles:1:1,guardian:1:1"
        KAFKA_URL_INSIDE="kafka:9093"
        NYT_API_KEY="API_KEY_OBTAINED_FROM_NYTIMES_DEVELOPER_ACCOUNT"
        GUARDIAN_API_KEY = "API_KEY_OBTAINED_FROM_GUARDIAN_DEVELOPER_ACCOUNT"
        ```

3. **Build and Run Services**:
    
    ```bash
    docker-compose up --build
    ```

    **Note**: Wait about 30 seconds for all containers to initialize.
    
4. **Access the API**:
    
    - The FastAPI documentation is available at `http://localhost:8000/docs`.

5. **Access the website**:

    - The NewsFlash website can be accessed at `http://localhost:8080/#`.

---

## Usage

### API Endpoints
All of these endpoints would be under different news sources /asianews /nytimes /guardian (considered as newssource for showing the endpoints for documentation)
- **GET newssource/**: Retrieve all the articles.
- **GET newssource/categories**: Retrieve all categories.
- **GET newssource/date**: Retrieve all articles by date.
- **GET newssource/today**: Retrieve the latest articles.
- **GET newssource/{category}**: Retrieve the articles for a specific category.
- **GET newssource/today/{category}**: Retrieve the latest articles for a specific category.

### Example Request

```bash
curl -X GET "http://localhost:8000/nytimes" -H "accept: application/json"
```

---

## System Workflow

1. **Data Collection**:
    - Collection containers fetch data from APIs or scrape websites.
    - Data is processed into a standardized JSON format.
2. **Kafka Topics**:
    - Each source has a dedicated Kafka topic.
    - Data is published to these topics asynchronously.
3. **Database Storage**:
    - PostgreSQL stores articles with fields like `title`, `category`, `image`, `link`, and `date`.
4. **API Access**:
    - FastAPI routes provide structured access to the stored data.

---

## Fault Tolerance and Scalability

- **Kafka**: Replication and partitioning ensure data availability and scalability.
- **PostgreSQL**: Supports horizontal scaling and transactional integrity.
- **Modular API**: Easily extendable to include new news sources or features.
- **Redis**: Added extra fault tolerance.

---

## Future Enhancements

- User authentication and personalized news feeds.
- Integration with NoSQL databases for handling semi-structured data.
- Kubernetes deployment for higher scalability.
- Advanced filtering and search capabilities for news articles.

---

## Contributors

- **Sujoy Dcunha**: Database setup, API design, Kafka broker scripting, Redis.
- **Zhao Xuqing**: Frontend development, API design.
- **Michael Glennon**: API design, data collection services, Documentation.
- **Ayan Mulla**: API integration, data collection services, Redis, Documentation.
