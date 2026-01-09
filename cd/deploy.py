#!/usr/bin/env python3

import subprocess
import sys
from datetime import datetime
from pathlib import Path

APP_DIR = "/opt/backend"
COMPOSE_FILE = f"{APP_DIR}/docker-compose.yml"
LOG_FILE = f"{APP_DIR}/deploy.log"
AWS_REGION = "us-east-2"
ECR_REGISTRY = "589335871756.dkr.ecr.us-east-2.amazonaws.com"

LOG_PREFIX = "[DEPLOY]"


def log(msg: str):
    timestamp = datetime.utcnow().isoformat()
    line = f"{timestamp} {LOG_PREFIX} {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def run(cmd: str):
    log(f"$ {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.stdout:
        log(result.stdout.strip())

    if result.returncode != 0:
        log(f"ERROR: {result.stderr.strip()}")
        sys.exit(result.returncode)


def main():
    log("🚀 Backend deployment started")

    # 1️ Preconditions
    if not Path(COMPOSE_FILE).exists():
        log(f"ERROR: Missing {COMPOSE_FILE}")
        sys.exit(1)

    run("docker compose version")

    # 2️ Authenticate to ECR
    log("🔐 Logging into Amazon ECR")
    run(
        f"aws ecr get-login-password --region {AWS_REGION} "
        f"| docker login --username AWS --password-stdin {ECR_REGISTRY}"
    )

    # 3️ Pull latest images
    log("⬇️ Pulling latest images")
    run(f"cd {APP_DIR} && docker compose pull")

    # 4️ Restart services
    log("🔄 Restarting backend services")
    run(f"cd {APP_DIR} && docker compose down")
    run(f"cd {APP_DIR} && docker compose up -d")

    # 5️ Verify containers
    log("🔍 Verifying running containers")
    result = subprocess.run(
        f"cd {APP_DIR} && docker compose ps --status running",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if "running" not in result.stdout.lower():
        log("ERROR: No running containers detected")
        log(result.stdout)
        sys.exit(1)

    log("📦 Running containers:")
    run("docker ps")

    log("✅ Backend deployment completed successfully")


if __name__ == "__main__":
    main()
