import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI, OpenAIError

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")

app = FastAPI(title="AGRI VOICE API", version="1.0.0")

# Local development only. Restrict these origins further when deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language: Literal["ta", "en", "hi"] = "ta"
    history: list[ChatMessage] = Field(default_factory=list, max_length=12)

class ChatResponse(BaseModel):
    answer: str

LANGUAGE_NAMES = {
    "ta": "Tamil",
    "en": "Indian English",
    "hi": "Hindi",
}

AGRI_INSTRUCTIONS = """
You are AGRI VOICE, a careful, friendly agricultural information assistant
designed for farmers in India.

Conversation rules:
- Reply in the language selected by the user: Tamil, Indian English, or Hindi.
- Use simple, respectful, everyday language. Avoid unnecessary technical terms.
- Ask short follow-up questions when crop, location, growth stage, symptoms,
  soil type, or timing is needed to understand the question.
- Be clear about uncertainty. Do not claim a crop disease is confirmed from
  a short description alone.
- Do not invent current market prices, weather, government scheme deadlines,
  eligibility, or official announcements. Explain that live data is not connected
  yet and direct the user to the relevant official source or local agriculture office.
- Do not invent research, sources, or facts.
- Do not prescribe pesticide or chemical use, mixtures, or dosages. For pest,
  disease, fertilizer, or other high-impact decisions, recommend confirmation
  with a qualified agricultural officer or agricultural university extension service.
- For urgent crop-loss concerns, encourage the farmer to contact the local
  agriculture department / extension officer promptly.
- Give practical, low-risk general information where appropriate.
- Keep answers concise and easy to understand, preferably with a few short steps.
- You are an information assistant, not a substitute for a qualified agronomist.
"""

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "AGRI VOICE API",
        "model_configured": bool(API_KEY),
        "model": MODEL,
    }

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is not configured on the backend."
        )

    # Keep only a small, validated conversation history.
    conversation = [
        {"role": item.role, "content": item.content}
        for item in request.history[-12:]
    ]
    conversation.append({"role": "user", "content": request.message})

    try:
        client = OpenAI(api_key=API_KEY)
        response = client.responses.create(
            model=MODEL,
            instructions=(
                AGRI_INSTRUCTIONS
                + f"\nThe selected response language is {LANGUAGE_NAMES[request.language]}."
            ),
            input=conversation,
        )
        answer = (response.output_text or "").strip()
        if not answer:
            raise HTTPException(
                status_code=502,
                detail="The AI returned an empty response. Please try again."
            )
        return ChatResponse(answer=answer)

    except OpenAIError:
        # Do not expose API keys, request headers, or raw provider details.
        raise HTTPException(
            status_code=502,
            detail="The AI service could not complete the request. Check API access and try again."
        )
