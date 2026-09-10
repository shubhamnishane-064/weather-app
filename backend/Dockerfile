FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for healthchecks (optional but recommended)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY app.py .

EXPOSE 5001

# DO NOT SET THE API KEY HERE.
# The key will be injected at runtime via environment variable.

CMD ["python", "app.py"]