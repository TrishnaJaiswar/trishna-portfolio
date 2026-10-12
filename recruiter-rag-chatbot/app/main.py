import os
from pathlib import Path
from typing import List

import numpy as np
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
KNOWLEDGE_FILE = ROOT / "data" / "profile.md"

app = FastAPI(title="Trishna Recruiter RAG Chatbot", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your portfolio domain before production deployment.
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1000)
    history: List[dict] = Field(default_factory=list, max_length=12)

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]


def load_chunks() -> list[str]:
    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")
    # Split by headings so each retrieved unit stays topic-focused.
    sections = []
    current = []
    for line in text.splitlines():
        if line.startswith("## ") and current:
            sections.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append("\n".join(current).strip())
    return [section for section in sections if len(section) > 30]

CHUNKS = load_chunks()
# First run downloads the compact embedding model from Hugging Face.
EMBEDDER = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
CHUNK_VECTORS = EMBEDDER.encode(CHUNKS, normalize_embeddings=True)


def retrieve(question: str, top_k: int = 4):
    q_vector = EMBEDDER.encode([question], normalize_embeddings=True)[0]
    scores = np.dot(CHUNK_VECTORS, q_vector)
    indices = np.argsort(scores)[::-1][:top_k]
    return [(CHUNKS[int(i)], float(scores[int(i)])) for i in indices]


def fallback_answer(question: str, retrieved: list[tuple[str, float]]) -> str:
    # Safe fallback if no Groq key is configured or the provider is unavailable.
    relevant = [chunk for chunk, score in retrieved if score >= 0.22]
    if not relevant:
        return ("I couldn't find that detail in Trishna's profile, so I don't want to guess. "
                "Please contact him directly at trishnajaiswar35@gmail.com.")
    excerpts = "\n\n".join(chunk for chunk in relevant[:3])
    return ("I found these relevant details in Trishna's profile. The AI-generated answer service is "
            "not configured right now, so here are the source notes instead:\n\n" + excerpts)


def generate_answer(question: str, retrieved: list[tuple[str, float]], history: list[dict]) -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    context = "\n\n---\n\n".join(chunk for chunk, _ in retrieved)
    if not api_key or api_key == "your_groq_api_key_here":
        return fallback_answer(question, retrieved)

    messages = [{
        "role": "system",
        "content": (
            "You are Trishna Jaiswar's recruiter-facing portfolio assistant. Answer questions about Trishna "
            "using ONLY the supplied context. Do not claim to be Trishna. Do not invent work experience, "
            "grades, certifications, metrics, salary, availability, or missing facts. If context lacks the answer, "
            "say the profile does not specify it and share his email. Be professional, concise, and useful to a recruiter. "
            "When relevant, mention project names and links exactly as given.\n\nPROFILE CONTEXT:\n" + context
        )
    }]
    # Only retain simple, valid recent conversation messages to limit prompt injection surface.
    for item in history[-6:]:
        role = item.get("role")
        content = item.get("content")
        if role in ("user", "assistant") and isinstance(content, str):
            messages.append({"role": role, "content": content[:1200]})
    messages.append({"role": "user", "content": question})
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                  "messages": messages, "temperature": 0.2, "max_tokens": 500},
            timeout=35,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return fallback_answer(question, retrieved)



def sse_event(payload: dict) -> str:
    return "data: " + json.dumps(payload, ensure_ascii=False) + "\n\n"

@app.post("/api/chat/stream")
def chat_stream(payload: ChatRequest):
    retrieved = retrieve(payload.question)
    sources = []
    for chunk, score in retrieved:
        if score >= 0.18:
            heading = next((line.removeprefix("## ") for line in chunk.splitlines() if line.startswith("## ")), "Profile")
            if heading not in sources:
                sources.append(heading)
    sources = sources[:4]

    def generate():
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        context = "\n\n---\n\n".join(chunk for chunk, score in retrieved if score >= 0.18)
        if not context:
            answer = "I couldn't find that detail in Trishna's profile, so I don't want to guess. Please contact him at trishnajaiswar35@gmail.com."
            for word in answer.split(" "):
                yield sse_event({"token": word + " "})
            yield sse_event({"sources": sources})
            return
        if not api_key or api_key == "your_groq_api_key_here":
            answer = fallback_answer(payload.question, retrieved)
            for word in answer.split(" "):
                yield sse_event({"token": word + " "})
            yield sse_event({"sources": sources})
            return
        messages = [{"role": "system", "content": (
            "You are Trishna Jaiswar's recruiter-facing portfolio assistant. Answer using ONLY the supplied profile context. "
            "Write natural, well-formatted Markdown like a helpful ChatGPT response: short paragraphs, **bold** for key terms, "
            "and concise bullet lists when useful. Never output raw HTML or Markdown tables. Do not claim to be Trishna. "
            "Never invent experience, grades, metrics, salary, or missing facts. If context lacks an answer, say so and share his email. "
            "Preserve project names and links exactly as provided.\n\nPROFILE CONTEXT:\n" + context
        )}]
        for item in payload.history[-6:]:
            role, content = item.get("role"), item.get("content")
            if role in ("user", "assistant") and isinstance(content, str):
                messages.append({"role": role, "content": content[:1200]})
        messages.append({"role": "user", "content": payload.question})
        try:
            with requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), "messages": messages,
                      "temperature": 0.2, "max_tokens": 700, "stream": True},
                timeout=(10, 90), stream=True) as response:
                response.raise_for_status()
                for raw_line in response.iter_lines(decode_unicode=True):
                    if not raw_line or not raw_line.startswith("data:"):
                        continue
                    data = raw_line[5:].strip()
                    if data == "[DONE]": break
                    try:
                        packet = json.loads(data)
                        token = packet["choices"][0].get("delta", {}).get("content")
                        if token: yield sse_event({"token": token})
                    except (ValueError, KeyError, IndexError, TypeError):
                        continue
            yield sse_event({"sources": sources})
        except Exception:
            answer = fallback_answer(payload.question, retrieved)
            for word in answer.split(" "):
                yield sse_event({"token": word + " "})
            yield sse_event({"sources": sources})

    return StreamingResponse(generate(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache", "X-Accel-Buffering": "no"
    })

@app.get("/health")
def health():
    return {"status": "ok", "knowledge_sections": len(CHUNKS), "llm_configured": bool(os.getenv("GROQ_API_KEY"))}

@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    retrieved = retrieve(payload.question)
    answer = generate_answer(payload.question, retrieved, payload.history)
    sources = []
    for chunk, score in retrieved:
        if score >= 0.18:
            heading = next((line.removeprefix("## ") for line in chunk.splitlines() if line.startswith("## ")), "Profile")
            if heading not in sources:
                sources.append(heading)
    return ChatResponse(answer=answer, sources=sources[:4])

# API-only backend: the portfolio website keeps and uses its existing embedded chatbot UI.
