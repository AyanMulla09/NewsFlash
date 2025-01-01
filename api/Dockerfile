FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["sh", "-c", "sleep 32 && uvicorn main:app --log-level debug --host 0.0.0.0 --port 8000"]
