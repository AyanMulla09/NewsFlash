FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
# CMD ["sh", "-c", "sleep 10 && uvicorn main:app --host 0.0.0.0 --port 8000"]
CMD ["sh", "-c", "sleep 5 && uvicorn main:app --log-level debug --host 0.0.0.0 --port 8000"]
