FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y awscli jq && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy shared entrypoint (from repo root context)
COPY backend/shared/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Install dependencies
COPY backend/ai-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ai-service/main.py .

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
