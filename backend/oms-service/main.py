from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from uuid import uuid4

app = FastAPI(title="Order Management Service")

# ---------- Secret Handling ----------
def read_secret(name: str) -> str | None:
    path = Path(f"/run/secrets/{name}")
    return path.read_text().strip() if path.exists() else None

JWT_SECRET = read_secret("jwt_secret")

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
