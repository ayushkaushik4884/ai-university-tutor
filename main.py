from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv


from rag_pipeline import ask_tutor
load_dotenv()

app = FastAPI(title="Jiit Tutor");

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    subject: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    response = ask_tutor(question=request.question, subject =request.subject)
    return ChatResponse(answer=response)