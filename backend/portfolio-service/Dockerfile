FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y awscli jq && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Copy shared entrypoint
COPY ../shared/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
