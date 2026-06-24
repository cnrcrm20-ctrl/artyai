from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uuid

from memory import init_db, get_history, save_fact, get_all_facts
from agent import chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="ArtyAI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class FactRequest(BaseModel):
    key: str
    value: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    result = await chat(session_id, req.message)
    return {"session_id": session_id, **result}

@app.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    history = await get_history(session_id, limit=50)
    return {"session_id": session_id, "history": history}

@app.post("/memory/fact")
async def add_fact(req: FactRequest):
    await save_fact(req.key, req.value)
    return {"status": "saved", "key": req.key}

@app.get("/memory/facts")
async def list_facts():
    facts = await get_all_facts()
    return {"facts": facts}

@app.get("/health")
async def health():
    return {"status": "ok", "agent": "Arty"}
