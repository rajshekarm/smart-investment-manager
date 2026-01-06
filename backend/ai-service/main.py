from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="AI Intent Service")

# ---------- Secret Handling ----------
def read_secret(name: str) -> str | None:
    path = Path(f"/run/secrets/{name}")
    return path.read_text().strip() if path.exists() else None

OPENAI_API_KEY = read_secret("openai_api_key")

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
