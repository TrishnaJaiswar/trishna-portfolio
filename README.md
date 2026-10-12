<<<<<<< HEAD
# Trishna Jaiswar — AI Engineering Portfolio

A responsive, dark navy-and-blue portfolio focused on AI engineering, agentic workflows, RAG systems, and deployed projects. Built with plain HTML, CSS, and JavaScript.

## Run locally
Open `index.html` in a browser, or serve the folder with a static server:

```bash
python -m http.server 5500
```

Then open `http://localhost:5500`.

## Main portfolio files
- `index.html` — home, about, exact resume education details, skills, certificates, featured projects, other projects, music hobbies, embedded recruiter chat section, contact details, and resume/cover-letter download buttons.
- `style.css` — responsive portfolio styling.
- `script.js` — navigation and UI interactions.
- `project-details.css` — shared styling for detailed project pages.
- `resolveai.html` — full ResolveAI project overview, workflow, engineering considerations, technology stack, and architecture diagram.
- `neuroscholar.html` — full NeuroScholar AI overview, agent workflow, feature list, stack, API documentation links, and architecture diagram.
- `forgeblog.html` — full ForgeBlog AI overview, multi-agent pipeline, interface/output details, stack, and architecture diagram.
- `assets/` — portrait, certificates, three full-size architecture diagrams, `Trishna-Jaiswar-Resume.pdf`, and `Trishna-Jaiswar-Cover-Letter.pdf`.
- `recruiter-rag-chatbot/` — separate FastAPI RAG backend project for the embedded recruiter chat interface.

## Featured projects

### ResolveAI — Enterprise Agentic Support Copilot
- **Live demo:** https://resolveai-enterprise-support-copilot.trishnajaiswar35.workers.dev
- **GitHub:** https://github.com/TrishnaJaiswar/resolveai-enterprise-support-copilot-
- **Details page:** `resolveai.html`
- **Architecture image:** `assets/resolveai-architecture.png`
- LangGraph routing for knowledge-base, ticket, and direct-answer requests.
- Pinecone semantic retrieval and LLM-based evidence grading.
- Tavily web fallback when internal knowledge is insufficient, with web evidence grading.
- Grounded answers, explicit insufficient-evidence fallback, and human approval before support-ticket creation.
- Company-specific Pinecone namespaces are shown in the architecture for tenant data separation.
- Stack: Python, FastAPI, LangGraph, Groq LLM, Pinecone, Tavily, RAG, Docker.

### NeuroScholar AI — Agentic Multi-Document Research Intelligence
- **Live demo:** https://scholarly.trishnajaiswar35.workers.dev/
- **Backend API:** https://scholarly-uguj.onrender.com
- **API docs:** https://scholarly-uguj.onrender.com/docs
- **GitHub:** https://github.com/TrishnaJaiswar/NeuroScholar-AI
- **Details page:** `neuroscholar.html`
- **Architecture image:** `assets/neuroscholar-architecture.png`
- Multi-PDF research chat, literature review, paper comparison, trend analysis, and academic report generation.
- Hybrid retrieval combines FAISS semantic search and BM25 keyword search; multi-query retrieval improves document discovery.
- LangGraph workflow components include planning, retrieval, research, analysis, citation, and report generation.
- Source-aware citations/references where available; SQLite/SQLAlchemy persistence for research sessions; PDF report export.
- Stack: Python, FastAPI, LangGraph, LangChain, Groq, FAISS, BM25, Hugging Face Sentence Transformers, SQLite, SQLAlchemy, ReportLab, Cloudflare Workers, Render, Docker.

### ForgeBlog AI — Autonomous Multi-Agent Technical Blog Generator
- **Live demo:** https://forgeblog-ai.onrender.com
- **GitHub:** https://github.com/TrishnaJaiswar/ForgeBlog-AI
- **Details page:** `forgeblog.html`
- **Architecture image:** `assets/forgeblog-architecture.png`
- Router agent selects closed-book, hybrid, or open-book research mode.
- Tavily research builds an evidence pack when web research is needed.
- Orchestrator creates an outline and writing constraints; parallel writer agents generate sections.
- Reducer merges sections in order; image planner and Hugging Face FLUX image agent create supporting visuals.
- Streamlit interface includes live progress, Markdown preview/download, image preview, citations/sources, and execution logs.
- Stack: Python, LangGraph, Streamlit, OpenRouter, Tavily Search API, Hugging Face FLUX.1-dev.

## Project card behavior
The selected-work area contains **only the three featured project cards**. Each card links to a full in-portfolio project detail page with an overview, features/workflow, stack, and architecture image. The live demo and GitHub repository are separate links. **Ask Trishna AI is not a project card**; the recruiter chatbot remains as its own section further down the main portfolio page.

## Embedded recruiter chatbot
The portfolio contains an embedded `Ask Trishna AI` chat section, but it requires a deployed API to return live LLM answers.

1. Read `recruiter-rag-chatbot/README.md` to configure and run the FastAPI backend.
2. Deploy the backend and configure `GROQ_API_KEY` as a server-side environment variable.
3. In `index.html`, set `window.TRISHNA_CHAT_API_URL` to the deployed API base URL (no trailing slash).
4. Configure backend CORS to allow your portfolio domain.
5. Never place the Groq API key in frontend JavaScript.

## Education, other projects, and interests
Education is transcribed from the supplied resume:
- B.E. in Artificial Intelligence and Data Science — New Horizon Institute of Technology and Management (Mumbai University) · May 2026
- XII (HSC) — P. A. Menon College of Commerce & Science · 2022, 60%

Other projects listed on the portfolio include AI Smart Interview & Skill Coach, AI Command-Based Video Editor, Deskmate AI, AI Resume Analyzer, and FitPilot AI. Singing, guitar, and piano are listed as personal interests. Repository links are included only where known and supplied.

## Resume and cover letter downloads
The hero section and Education section link to the supplied PDF files in `assets/`. The buttons use relative paths and will work after deployment as long as the assets folder is uploaded with the site.

## Certificates and assets
The `assets/` folder includes the supplied portrait, certificates, and project architecture diagrams. Check that you want the supplied certificate PDFs to be public before deploying.

## Deploy
Deploy the portfolio folder to Cloudflare Pages, Netlify, GitHub Pages, or another static host. Keep the RAG API deployed separately if the chatbot uses FastAPI.


## Recruiter chatbot: local RAG + Groq streaming

The recruiter chat UI remains embedded in the portfolio. The backend lives in `recruiter-rag-chatbot/`; there is no separate chatbot page needed. Assistant answers render readable Markdown (paragraphs, headings, bold text, lists, and inline code) and stream as tokens arrive.

### Run locally (Windows PowerShell)
1. Open a terminal in `trishna-portfolio/recruiter-rag-chatbot`.
2. Activate your environment: `..\venv\Scripts\Activate.ps1` if your virtual environment is at the portfolio root, or create/activate a local `venv` in this folder.
3. Install backend dependencies: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and set `GROQ_API_KEY` and `GROQ_MODEL=openai/gpt-oss-120b`. Keep the real API key private.
5. Start the API from the `recruiter-rag-chatbot` folder: `uvicorn app.main:app --reload --port 8000`.
6. Serve the portfolio root (the folder containing `index.html`) with VS Code Live Server. The local chat API URL is configured to `http://127.0.0.1:8000`.
7. Visit the Live Server portfolio URL and test the existing “Ask Trishna AI” widget. The API health check is `http://127.0.0.1:8000/health`; `/docs` is API documentation, not the chatbot UI.

### Live deployment
Deploy `recruiter-rag-chatbot` as a Python web service and set its environment variables in the hosting dashboard. Then replace `window.TRISHNA_CHAT_API_URL` in `index.html` with the deployed backend base URL (no trailing slash). Restrict backend CORS to the actual portfolio domain before production. Never commit `.env` or expose the Groq key in browser JavaScript.
=======
# trishna-portfolio
>>>>>>> fc2942667eaea41d0669ec62c8acefa721430305
