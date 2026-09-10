FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/

EXPOSE 5000

ENV BACKEND_URL="http://backend-service:5001"

CMD ["python", "app.py"]
