from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import ZentroMartAgent
from src.rag_engine import KnowledgeBase
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ZentroMart VoiceOps AI API")

# Initialize AI components
kb = KnowledgeBase()
kb.ingest_documents()
agent = ZentroMartAgent(rag_engine=kb)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        reply = agent.process_turn(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)