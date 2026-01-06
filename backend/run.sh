#!/usr/bin/env bash
set -e

echo "🔐 Setting up Docker secrets..."

SECRETS_DIR="/opt/secrets"

sudo mkdir -p $SECRETS_DIR
sudo chown $(whoami) $SECRETS_DIR

# Create secrets ONLY if they don't exist
# ---------- AI Secret ----------
if [ ! -f "$SECRETS_DIR/openai_api_key" ]; then
  echo "sk-local-test-key" > $SECRETS_DIR/openai_api_key
  echo "Created openai_api_key"
else
  echo "openai_api_key already exists"
fi

# ---------- JWT Secret ----------
if [ ! -f "$SECRETS_DIR/jwt_secret" ]; then
  echo "local-jwt-secret" > $SECRETS_DIR/jwt_secret
  echo "Created jwt_secret"
else
  echo "jwt_secret already exists"
fi

# ---------- Postgres Secret ----------
if [ ! -f "$SECRETS_DIR/postgres_password" ]; then
  echo "local-postgres-password" > $SECRETS_DIR/postgres_password
  echo "Created postgres_password"
else
  echo "postgres_password already exists"
fi

chmod 600 $SECRETS_DIR/*

echo "🚀 Starting Docker Compose..."

docker-compose up -d --build
