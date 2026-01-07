#!/usr/bin/env python3

import subprocess
import sys
from datetime import datetime

APP_DIR = "/opt/backend"
LOG_PREFIX = "[DEPLOY]"


def run(cmd: str):
    print(f"{LOG_PREFIX} $ {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        sys.exit(result.returncode)

    if result.stdout:
        print(result.stdout)


def main():
    print(f"{LOG_PREFIX} 🚀 Backend deployment started")
    print(f"{LOG_PREFIX} ⏰ {datetime.utcnow().isoformat()} UTC")

    # 1️⃣ Sanity checks
    run("docker --version")
    run("docker-compose --version")

    # 2️⃣ Move to app directory
    run(f"cd {APP_DIR}")

    # 3️⃣ Pull latest images from ECR
    print(f"{LOG_PREFIX} 🔄 Pulling latest images from ECR")
    run(f"cd {APP_DIR} && docker-compose pull")

    # 4️⃣ Restart services safely
    print(f"{LOG_PREFIX} 🔁 Restarting backend services")
    run(f"cd {APP_DIR} && docker-compose down")
    run(f"cd {APP_DIR} && docker-compose up -d")

    # 5️⃣ Show running containers
    print(f"{LOG_PREFIX} 📦 Running containers")
    run("docker ps")

    print(f"{LOG_PREFIX} ✅ Backend deployment completed successfully")


if __name__ == "__main__":
    main()
  