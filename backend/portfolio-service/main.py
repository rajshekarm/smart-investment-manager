from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title="Portfolio Service")

# ---------- Models ----------

class Order(BaseModel):
    symbol: str = Field(..., example="AAPL")
    side: Literal["BUY", "SELL"]
    quantity: int = Field(..., gt=0)

class PositionResponse(BaseModel):
    symbol: str
    side: str
    quantity: int
    position_status: str


# ---------- Health ----------

@app.get("/health")
def health():
    return {
        "service": "portfolio-service",
        "status": "ok"
    }


# ---------- Business Logic ----------

@app.post("/update-position", response_model=PositionResponse)
def update_position(order: Order):
    """
    Updates portfolio position based on an executed order.
    (In production, this would persist to a DB.)
    """

    quantity_change = order.quantity if order.side == "BUY" else -order.quantity

    return PositionResponse(
        symbol=order.symbol,
        side=order.side,
        quantity=quantity_change,
        position_status="UPDATED"
    )
