from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from uuid import uuid4
import os

app = FastAPI(title="Order Management Service")

# ---------- Secret Handling ----------

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value

JWT_SECRET = require_env("JWT_SECRET")

# ---------- Models ----------
class Order(BaseModel):
    symbol: str
    side: str
    quantity: int
    price: float | None = None

# ---------- Endpoints ----------
@app.get("/health")
def health():
    return {
        "service": "oms-service",
        "status": "ok",
        "jwt_loaded": JWT_SECRET is not None
    }

@app.post("/orders")
def create_order(order: Order):
    return {
        "order_id": str(uuid4()),
        "status": "RECEIVED",
        "order": order
    }
