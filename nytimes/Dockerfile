FROM python:3.9-slim
RUN apt-get update && apt-get install -y cron
COPY crontab /etc/cron.d/crontab
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
CMD ["bash", "run.sh"]