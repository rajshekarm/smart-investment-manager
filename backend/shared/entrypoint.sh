#!/bin/sh
set -e

if [ -z "$SECRET_ID" ]; then
  echo "❌ SECRET_ID env var not set"
  exit 1
fi

echo "🔐 Loading secrets from AWS Secrets Manager: $SECRET_ID"

SECRET_JSON=$(aws secretsmanager get-secret-value \
  --secret-id "$SECRET_ID" \
  --query SecretString \
  --output text)

export $(echo "$SECRET_JSON" | jq -r 'to_entries|map("\(.key)=\(.value)")|.[]')

echo "✅ Secrets loaded. Starting application..."

exec "$@"
