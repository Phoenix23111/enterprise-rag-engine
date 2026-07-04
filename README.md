# 🎓 Enterprise RAG Microservice Architecture

A full-stack, production-grade, and fully containerized Retrieval-Augmented Generation (RAG) engine. This system decouples an intelligent AI orchestrator built with FastAPI and LlamaIndex from a lightning-fast React user interface served via Nginx. The entire ecosystem is orchestrated seamlessly using Docker Compose, leveraging stateful conversational memory and optimized CPU-bound embeddings.

---

## 🏗️ System Architecture

The application is built using a decoupled microservices architecture to ensure scalability, clean separation of concerns, and ease of deployment:

- **Frontend UI:** React (Vite) compiled into an optimized production build and served via an **Nginx** reverse-proxy container.
- **Backend API Gateway:** **FastAPI** running asynchronously with Uvicorn, featuring custom CORS middleware configuration to securely communicate with the frontend.
- **AI Orchestration:** **LlamaIndex** utilizing a stateful `ChatEngine` with an integrated `ChatMemoryBuffer` to maintain multi-turn conversational context.
- **Large Language Model:** Google **Gemini 2.5 Flash** for quick, accurate contextual synthesis.
- **Embeddings & Vector Database:** Local CPU-optimized HuggingFace embeddings (`BAAI/bge-small-en-v1.5`) mapped into an in-memory vector store index.
- **Container Orchestration:** **Docker Compose** managing isolated virtual networks and automated multi-stage builds.

---

## 🚀 Quickstart & Deployment

### 1. Prerequisites

Ensure you have the following installed on your host machine:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- A valid Google AI Studio Gemini API Key

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/enterprise-rag-engine.git
cd enterprise-rag-engine
```

> **Note:** Replace `yourusername` with your actual GitHub username.

### 3. Environment Configuration

Create a `.env` file in the project root (next to `docker-compose.yml`) and add your Gemini API key:

```env
GEMINI_API_KEY=AIzaSyYourActualGeminiApiKeyHere...
```

> The root `.gitignore` is configured to prevent this file from being committed.

### 4. Build and Launch

Build and start all services with:

```bash
docker compose up --build
```

After the containers start, access the application at:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API Docs (Swagger) | http://localhost:8000/docs |

To stop the application:

```bash
docker compose down
```


## 🧠 Key Engineering Decisions

### Multi-Stage Frontend Builds

The frontend uses a two-stage Docker build:

1. **Node.js** compiles the React application into optimized static assets.
2. **Nginx** serves the compiled files, eliminating the need to run a Node server in production.

This approach significantly reduces image size and improves security.

---

### Stateful Conversational Memory

Instead of using a stateless `QueryEngine`, the backend utilizes a LlamaIndex `ChatEngine` with `ChatMemoryBuffer`.

This enables:

- Multi-turn conversations
- Context retention
- Pronoun resolution
- More natural follow-up questions

---

### Asynchronous Backend

The FastAPI backend is built using Python's native `async`/`await` syntax, allowing efficient handling of concurrent requests while minimizing thread blocking during LLM interactions.

---

### Optimized CPU-Only PyTorch

To reduce Docker image size and avoid unnecessary CUDA dependencies, the project installs CPU-only PyTorch wheels using:

```text
--extra-index-url https://download.pytorch.org/whl/cpu
```

This optimization:

- Reduces container size
- Speeds up Docker builds
- Improves compatibility across operating systems
- Eliminates GPU dependency for local deployments

---

## 📌 Features

- ✅ Retrieval-Augmented Generation (RAG)
- ✅ FastAPI Backend
- ✅ React + Vite Frontend
- ✅ Dockerized Microservice Architecture
- ✅ Nginx Reverse Proxy
- ✅ LlamaIndex Chat Engine
- ✅ Stateful Chat Memory
- ✅ HuggingFace Embeddings
- ✅ Gemini 2.5 Flash Integration
- ✅ Interactive Swagger Documentation
- ✅ CPU-Optimized Deployment

---
