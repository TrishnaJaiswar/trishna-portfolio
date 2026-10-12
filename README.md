# Trishna Jaiswar | AI Engineering Portfolio

A responsive personal portfolio showcasing my work in **AI Engineering, Generative AI, Agentic AI, Retrieval-Augmented Generation (RAG), and multi-agent systems**. Built with HTML, CSS, and JavaScript, with dedicated project pages, architecture diagrams, live demos, and an embedded AI-powered recruiter chatbot.

## 🚀 Featured Projects

### 1. ResolveAI — Enterprise Agentic Support Copilot

An agentic AI support assistant designed to answer employee questions using enterprise knowledge bases, retrieve relevant evidence, and assist with support-ticket workflows.

- **Live Demo:** [ResolveAI](https://resolveai-enterprise-support-copilot.trishnajaiswar35.workers.dev)
- **GitHub:** [Repository](https://github.com/TrishnaJaiswar/resolveai-enterprise-support-copilot-)
- **Project Details:** `resolveai.html`

**Key Features**
- LangGraph-based workflow routing.
- Pinecone-powered enterprise knowledge retrieval.
- Evidence grading and grounded response generation.
- Tavily web search fallback when internal knowledge is insufficient.
- Human approval before support-ticket creation.
- Company-specific namespace design for tenant data separation.

**Tech Stack:** Python, FastAPI, LangGraph, Groq, Pinecone, Tavily, RAG, Docker.

### 2. NeuroScholar AI — Agentic Research Intelligence Platform

An AI-powered research platform for analyzing multiple academic documents, comparing papers, generating literature reviews, identifying research trends, and producing structured research reports.

- **Live Demo:** [NeuroScholar AI](https://scholarly.trishnajaiswar35.workers.dev/)
- **Backend API:** [Render API](https://scholarly-uguj.onrender.com)
- **API Documentation:** [Swagger UI](https://scholarly-uguj.onrender.com/docs)
- **GitHub:** [NeuroScholar-AI](https://github.com/TrishnaJaiswar/NeuroScholar-AI)
- **Project Details:** `neuroscholar.html`

**Key Features**
- Multi-document research and question answering.
- Hybrid retrieval using FAISS semantic search and BM25 keyword search.
- Multi-query retrieval for improved document discovery.
- LangGraph-powered planning, retrieval, research, analysis, and report generation.
- Source-aware citations and references where available.
- Persistent research sessions and PDF report export.

**Tech Stack:** Python, FastAPI, LangGraph, LangChain, Groq, FAISS, BM25, Hugging Face Sentence Transformers, SQLite, SQLAlchemy, ReportLab, Docker, Cloudflare Workers, Render.

### 3. ForgeBlog AI — Autonomous Multi-Agent Blog Generator

A multi-agent AI application that researches topics, plans technical articles, generates content in parallel, and creates supporting visuals.

- **Live Demo:** [ForgeBlog AI](https://forgeblog-ai.onrender.com)
- **GitHub:** [ForgeBlog-AI](https://github.com/TrishnaJaiswar/ForgeBlog-AI)
- **Project Details:** `forgeblog.html`

**Key Features**
- Intelligent routing between closed-book, hybrid, and open-book research modes.
- Web research and evidence collection using Tavily.
- Outline planning and writing constraints.
- Parallel section-writing agents with ordered output reduction.
- AI-generated supporting visuals using Hugging Face FLUX.
- Streamlit interface with progress updates, Markdown preview, downloads, sources, and execution logs.

**Tech Stack:** Python, LangGraph, Streamlit, OpenRouter, Tavily Search API, Hugging Face FLUX.1-dev.

---

## 💻 Portfolio Features

- Responsive design for desktop, tablet, and mobile.
- Home, About, Skills, Education, Projects, and Contact sections.
- Dedicated project detail pages with architecture diagrams.
- Live demo and GitHub links for featured projects.
- Resume and cover letter PDF downloads.
- Certificates and additional projects.
- Embedded **Ask Trishna AI** recruiter chatbot.
- Markdown-formatted chatbot responses with token streaming when supported by the deployed backend.

## 🛠️ Tech Stack

**Frontend**
- HTML5
- CSS3
- JavaScript

**AI & Machine Learning**
- Python
- Generative AI and LLMs
- Retrieval-Augmented Generation (RAG)
- Agentic AI and multi-agent workflows
- LangChain and LangGraph
- FAISS and BM25
- Hugging Face

**Backend & Data**
- FastAPI
- REST APIs
- MongoDB and SQL databases
- SQLite and SQLAlchemy
- Pinecone

**Tools & Deployment**
- Git and GitHub
- Docker
- Cloudflare Workers
- Render
- Streamlit

## 📁 Project Structure

```text
trishna-portfolio/
├── index.html
├── style.css
├── script.js
├── project-details.css
├── resolveai.html
├── neuroscholar.html
├── forgeblog.html
├── assets/
│   ├── Trishna-Jaiswar-Resume.pdf
│   ├── Trishna-Jaiswar-Cover-Letter.pdf
│   ├── resolveai-architecture.png
│   ├── neuroscholar-architecture.png
│   ├── forgeblog-architecture.png
│   └── certificates and images
└── recruiter-rag-chatbot/
    ├── app/
    ├── requirements.txt
    └── README.md
```

*The structure above represents the main portfolio files. Supporting files and folders may vary by version.*

## ▶️ Run Locally

### Prerequisites

- Git
- Python 3.x (for the local static server and chatbot backend)
- A modern web browser

### 1. Clone the repository

```bash
git clone <YOUR-PORTFOLIO-REPOSITORY-URL>
cd trishna-portfolio
```

Replace the placeholder with your actual portfolio GitHub repository URL.

### 2. Start the portfolio

Run this command from the directory containing `index.html`:

```bash
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

Alternatively, open `index.html` directly in your browser or use VS Code Live Server.

## 🤖 Ask Trishna AI — Recruiter Chatbot

The portfolio includes an embedded AI chatbot designed to help recruiters explore my background, technical skills, projects, and experience.

The chatbot uses a separate FastAPI backend with retrieval-augmented generation and Groq-powered responses.

### Run the backend locally

1. Open a terminal in `recruiter-rag-chatbot/`.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`.
5. Configure the required environment variables:

   ```env
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=openai/gpt-oss-120b
   ```

6. Start the API:

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

7. Check the health endpoint:

   ```text
   http://127.0.0.1:8000/health
   ```

8. Open the portfolio using Live Server and test the embedded chatbot.

### Deploy the chatbot

- Deploy the FastAPI backend separately using a Python-compatible hosting service.
- Configure API keys as server-side environment variables.
- Set `window.TRISHNA_CHAT_API_URL` in `index.html` to the deployed backend URL, without a trailing slash.
- Configure CORS to allow requests from the portfolio domain.
- Never expose API keys in frontend JavaScript or commit `.env` files.

For backend-specific instructions, see `recruiter-rag-chatbot/README.md`.

## 🎓 Education

**Bachelor of Engineering — Artificial Intelligence and Data Science**  
New Horizon Institute of Technology and Management, Mumbai University  
Graduated: May 2026

**Higher Secondary Certificate (HSC)**  
P. A. Menon College of Commerce & Science  
2022

## 🧩 Additional Projects

Other projects featured in the portfolio include:

- AI Smart Interview & Skill Coach
- AI Command-Based Video Editor
- Deskmate AI
- AI Resume Analyzer
- FitPilot AI

Visit the portfolio's Projects section for the available descriptions and links.

## 📄 Resume & Certificates

The portfolio provides access to my resume, cover letter, certificates, and project architecture diagrams through the `assets/` directory.

Only include documents and certificates you intend to make publicly accessible.

## 🌐 Deployment

The frontend is a static website and can be deployed using:

- Cloudflare Pages
- GitHub Pages
- Netlify
- Other static hosting platforms

The recruiter chatbot requires a separately deployed backend if live AI responses are enabled.

## 📬 Contact

**Trishna Jaiswar**  
AI Engineer | Generative AI | Agentic AI | RAG Systems

- **GitHub:** [github.com/TrishnaJaiswar](https://github.com/TrishnaJaiswar)
- **LinkedIn:** [Connect with me on LinkedIn](https://www.linkedin.com/)

For professional inquiries, use the contact information provided on my portfolio.

---

*Building practical AI systems that combine LLMs, retrieval, agentic workflows, and real-world applications.*
