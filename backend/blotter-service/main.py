from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Trade Blotter Service")

@app.get("/health")
def health():
    return {
        "service": "blotter-service",
        "status": "ok"
    }

@app.get("/trades")
def get_trades():
    return [
        {
            "trade_id": "TRD-001",
            "symbol": "AAPL",
            "side": "BUY",
            "quantity": 100,
            "price": 180.0,
            "timestamp": datetime.utcnow().isoformat()
        }
    ]
