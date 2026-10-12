# Trishna Recruiter RAG Chatbot

A recruiter-facing portfolio assistant that answers questions about Trishna's skills and AI projects using a profile knowledge base. It retrieves relevant profile sections with Sentence Transformers embeddings, then uses Groq chat completions to write a concise answer grounded in those sections. Retrieved section names are returned as source labels.

## Features
- Semantic retrieval from `data/profile.md` using `all-MiniLM-L6-v2` embeddings.
- Groq API integration; API key stays on the backend in `.env`.
- Source-section labels returned with answers.
- Guardrails against inventing experience, metrics, grades, certifications, and missing details.
- Fallback profile excerpts when no Groq key is configured or the provider is unavailable.
- FastAPI endpoint, health check, and responsive recruiter chat UI.

## Run locally (Windows PowerShell)

```powershell
cd recruiter-rag-chatbot
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `GROQ_API_KEY` using a key from https://console.groq.com/keys. Then run:

```powershell
uvicorn app.main:app --reload
```

The API-only backend runs at http://127.0.0.1:8000. Health check: http://127.0.0.1:8000/health. API docs: http://127.0.0.1:8000/docs. Open the portfolio `index.html` with Live Server to use the existing embedded chatbot UI. When frontend and backend use different hosts, set `window.TRISHNA_CHAT_API_URL` to the deployed backend base URL before `script.js` loads.

The first launch downloads the embedding model from Hugging Face. Without a Groq key, retrieval still runs and the app returns relevant source notes instead of generated prose.

## API

`POST /api/chat`

```json
{
  "question": "Explain ResolveAI's RAG architecture.",
  "history": []
}
```

## Deploy
Deploy the FastAPI app to a Python host (for example Render) using build command `pip install -r requirements.txt` and start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Set `GROQ_API_KEY` and `GROQ_MODEL` in the host's environment settings. Restrict CORS in `app/main.py` to your portfolio domain before production. After deployment, add the deployed URL to the portfolio project card.

## Update the knowledge base
Edit `data/profile.md` when projects, links, skills, or contact details change. Restart the service after editing because embeddings are created at startup. Do not add private information that should not be shared with recruiters.
