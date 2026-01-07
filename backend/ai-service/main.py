from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os

app = FastAPI(title="AI Intent Service")

# ---------- Secret Handling ----------

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value

JWT_SECRET = require_env("JWT_SECRET")

OPENAI_API_KEY = require_env("openai_api_key")

# ---------- Middleware ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class UserIntent(BaseModel):
    message: str

class OrderIntent(BaseModel):
    symbol: str
    side: str
    quantity: int
    price: float | None = None

# ---------- Endpoints ----------
@app.get("/health")
def health():
    return {
        "service": "ai-service",
        "status": "ok",
        "llm_key_loaded": OPENAI_API_KEY is not None
    }

@app.post("/interpret", response_model=OrderIntent)
def interpret_intent(intent: UserIntent):
    """
    TODO : MOCK LLM logic – replace with OpenAI/Gemini call later 
    """
    return OrderIntent(
        symbol="AAPL",
        side="BUY",
        quantity=100,
        price=180.0
    )
