# FarmaSense 🌱

<div align="center">

![FarmaSense Banner](https://img.shields.io/badge/FarmaSense-Intelligent%20Agriculture-2ECC71?style=for-the-badge&logo=leaf&logoColor=white)

[![React](https://img.shields.io/badge/React-19.x-61DAFB?style=flat-square&logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb)](https://www.mongodb.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Groq-FF6B35?style=flat-square)](https://python.langchain.com/)
[![Redis](https://img.shields.io/badge/Redis-Semantic%20Cache-DC382D?style=flat-square&logo=redis)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-Workers-37814A?style=flat-square)](https://docs.celeryq.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

**An AI-powered agricultural intelligence platform designed to empower Indian farmers with smart crop advisories, real-time alerts, and a multilingual AI assistant.**

[Farmer Portal](#-farmer-portal) · [Admin Dashboard](#-admin-dashboard) · [Architecture](#-architecture) · [API Docs](#-api-endpoints) · [Getting Started](#-getting-started)

</div>

---

## 📖 Overview

FarmaSense bridges the gap between modern AI and traditional farming. Farmers can register their farms, get AI-generated crop recommendations grounded in a real agricultural knowledge base via RAG, receive proactive weather & market alerts, and converse with an intelligent agricultural assistant — all in their **native Indian language**, right from their mobile phone.

---

## ✨ Features

### 🧑‍🌾 Farmer Portal
- **OTP-Based Authentication** — Secure mobile number login, no password required
- **Farm Registration** — Add farms with auto-location via IPGeolocation API
- **AI Crop Advisory** — LangGraph state machine + Groq-powered recommendations tailored to soil, district, season, and land size — grounded by RAG over a crop/soil knowledge base
- **Multilingual AI Chat** — Converse with the farm assistant in 13 Indian languages (Hindi, Marathi, Gujarati, Tamil, Telugu, and more)
- **PWA with Offline Mode** — Works in low-signal conditions; advisories cached locally for field use
- **Mobile-First Design** — Glassmorphism UI with bottom navigation bar, loading skeletons, and clear error states optimised for smartphones
- **Proactive Weather Alerts** — Weather-triggered push notifications automatically surface crop protection advisories before farmers need to ask

### 🛡️ Admin Dashboard
- **Secure Admin Login** — JWT-protected admin portal
- **Farmer Management** — View all registered farmers
- **Advisory Overview** — Monitor all AI-generated advisories
- **Alert Management** — View & manage system alerts
- **Platform Analytics** — Visual insights with Recharts

### 🔧 Platform Infrastructure
- **RESTful API** — FastAPI backend with modular route structure
- **JWT Authentication** — Stateless secure token-based auth for both farmers and admins
- **MongoDB Atlas** — Flexible NoSQL database with enforced schemas via Beanie ODM and Atlas Vector Search for RAG
- **Async Task Queue** — Celery + Redis workers for reliable background jobs with dead letter queue for failed SMS alerts
- **Redis Semantic Cache** — Deduplicates repeated LLM calls; reduces Groq API costs and latency
- **SMS / WhatsApp Alerts** — Twilio integration with retry logic for critical farm notifications
- **CI/CD Pipeline** — GitHub Actions with lint, test, and coverage gates on every merge

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js 19, React Router v7, Axios, PWA (Service Worker) |
| **Styling** | Vanilla CSS (mobile-first, glassmorphism) |
| **Maps** | Leaflet + React-Leaflet |
| **Charts** | Recharts |
| **Backend** | Python 3.9+, FastAPI |
| **Task Queue** | Celery + Redis |
| **Database** | MongoDB Atlas (Beanie ODM) + Atlas Vector Search |
| **Caching** | Redis (semantic similarity cache for LLM calls) |
| **AI / LLM** | LangGraph, LangChain, ChatGroq (`llama-3.1-8b-instant`) |
| **RAG** | MongoDB Atlas Vector Search + LangChain embeddings |
| **Data Validation** | Pydantic v2 |
| **Authentication** | JWT (python-jose) |
| **Geolocation** | IPGeolocation.io API |
| **Notifications** | Twilio (SMS/WhatsApp) with tenacity retry |
| **Testing** | Pytest, pytest-asyncio, coverage |
| **CI/CD** | GitHub Actions |

---

## 🗂️ Project Structure

```
farmasense/
│
├── .github/
│   └── workflows/
│       └── ci.yml                   # Lint, test, coverage gate on every PR
│
├── frontend/                        # React PWA Application
│   ├── public/
│   │   ├── manifest.json            # PWA manifest
│   │   └── service-worker.js        # Offline caching strategy
│   └── src/
│       ├── components/
│       │   ├── AdminLayout.js       # Admin navigation wrapper
│       │   ├── FarmerLayout.js      # Farmer bottom nav (mobile-first)
│       │   └── Skeleton.js          # Loading skeleton components
│       ├── context/
│       │   └── AuthContext.js       # Global auth state (farmer + admin)
│       ├── pages/
│       │   ├── admin/               # Admin portal pages
│       │   │   ├── AdminLogin.js
│       │   │   ├── Dashboard.js
│       │   │   ├── Farmers.js
│       │   │   ├── Advisories.js
│       │   │   ├── Alerts.js
│       │   │   └── Analytics.js
│       │   └── farmer/              # Farmer portal pages
│       │       ├── Login.js         # Mobile OTP login
│       │       ├── FarmerDashboard.js
│       │       ├── MyFarms.js
│       │       ├── AddFarm.js       # Farm registration + GPS location
│       │       └── FarmDetails.js   # AI advisory + multilingual chat
│       └── services/
│           └── api.js               # Centralized Axios API client
│
└── backend/                         # FastAPI Application
    ├── app/
    │   ├── agents/
    │   │   ├── advisory_agent.py    # LangGraph node — crop advisory generation
    │   │   ├── chat_agent.py        # LangGraph node — multilingual chat
    │   │   ├── guardrails.py        # Prompt injection defense + output validation
    │   │   └── graph.py             # LangGraph state machine orchestration
    │   ├── models/
    │   │   └── schemas.py           # Pydantic v2 models (request + response)
    │   ├── db/
    │   │   ├── documents.py         # Beanie ODM document definitions
    │   │   └── indexes.py           # MongoDB index declarations
    │   ├── routes/
    │   │   ├── auth.py              # OTP send/verify endpoints
    │   │   ├── farm.py              # Farm CRUD + geolocation proxy
    │   │   ├── advisory.py          # AI advisory generation + chat
    │   │   ├── alerts.py            # Alerts management
    │   │   ├── market.py            # Mandi price API
    │   │   └── admin.py             # Admin-only protected routes
    │   ├── workers/
    │   │   ├── celery_app.py        # Celery + Redis worker config
    │   │   ├── alert_tasks.py       # Scheduled alert jobs with DLQ
    │   │   └── weather_tasks.py     # Weather-triggered advisory jobs
    │   ├── cache/
    │   │   └── semantic_cache.py    # Redis semantic similarity cache for LLM
    │   └── __init__.py              # App factory + MongoDB + Beanie init
    ├── tests/
    │   ├── test_auth.py             # Auth route unit tests
    │   ├── test_advisory.py         # Advisory + chat route tests (mocked LLM)
    │   ├── test_farm.py             # Farm CRUD tests
    │   └── conftest.py              # Pytest fixtures + async test client
    ├── seed.py                      # MongoDB seed script (mock data)
    ├── .env.example                 # Example environment variables (commit this)
    ├── requirements.txt
    └── run.py                       # App entry point
```

---

## 🗄️ MongoDB Collections

| Collection | Description |
|---|---|
| `admins` | Admin credentials (hashed passwords) |
| `users` | Farmer profiles (mobile, name, language preference) |
| `farms` | Farm details (location, soil, size, water source) — indexed on `user_id` |
| `advisories` | AI-generated crop recommendation summaries — indexed on `farm_id`, `created_at` |
| `advisory_reports` | Full AI advisory JSON payloads — Pydantic-validated before write |
| `advisory_embeddings` | Crop/soil knowledge vectors for Atlas Vector Search RAG |
| `alerts` | Weather/market alerts sent to farmers — indexed on `user_id`, `created_at` |

---

## 🏗️ Architecture

### AI Pipeline (LangGraph)

```
User request
     │
     ▼
Guardrails layer (prompt injection check)
     │
     ▼
Redis semantic cache ──► Cache hit → return immediately
     │ Cache miss
     ▼
LangGraph state machine
  ├── advisory_agent  (RAG → Atlas Vector Search → Groq LLM)
  └── chat_agent      (language detection → Groq LLM → multilingual response)
     │
     ▼
Pydantic output validation
     │
     ▼
Store in MongoDB + update cache
```

### Background Jobs (Celery)

```
Celery beat scheduler
  ├── weather_tasks   → fetch weather → trigger proactive advisory → WhatsApp/SMS
  └── alert_tasks     → send alerts → Twilio (tenacity retry) → DLQ on failure
```

---

## 🚀 Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) v18+
- [Python](https://python.org/) v3.9+
- [MongoDB Atlas](https://www.mongodb.com/) account (for Vector Search)
- [Redis](https://redis.io/) (local or managed)
- [Git](https://git-scm.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/swastik3616/Farmasense.git
cd Farmasense
```

### 2. Backend Setup

```bash
cd backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Copy and fill in the environment file:

```bash
cp .env.example .env
```

```env
# FastAPI
SECRET_KEY=your_secret_key

# MongoDB Atlas
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/farmasense

# Redis
REDIS_URL=redis://localhost:6379/0

# Groq AI
GROQ_API_KEY=your_groq_api_key

# IPGeolocation
GEOLOCATION_API_KEY=your_ipgeolocation_api_key

# Twilio
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx

# OpenWeatherMap
WEATHER_API_KEY=your_openweathermap_key
```

Seed the database and build the vector index:

```bash
python seed.py
```

Start the API server and Celery worker in separate terminals:

```bash
# Terminal 1 — FastAPI server
python run.py

# Terminal 2 — Celery worker
celery -A app.workers.celery_app worker --loglevel=info

# Terminal 3 — Celery beat scheduler (for periodic tasks)
celery -A app.workers.celery_app beat --loglevel=info
```

> API will be accessible at `http://localhost:8000`  
> Interactive docs at `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

> App opens at `http://localhost:3000`

### 4. Run Tests

```bash
cd backend
pytest --cov=app tests/ --cov-report=term-missing
```

---

## 🌐 Accessing the Portals

| Portal | URL | Credentials |
|--------|-----|-------------|
| **Farmer Portal** | `http://localhost:3000/farmer/login` | Any 10-digit mobile + OTP (check backend console) |
| **Admin Dashboard** | `http://localhost:3000/admin/login` | `admin@farmasense.com` / `admin123` |
| **API Docs (Swagger)** | `http://localhost:8000/docs` | — |

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/send-otp` | Send OTP to farmer mobile |
| `POST` | `/api/auth/verify-otp` | Verify OTP and get JWT token |

### Farm
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/farm/` | Get all farms for current user |
| `POST` | `/api/farm/create` | Register a new farm |
| `GET` | `/api/farm/{id}` | Get a specific farm |
| `GET` | `/api/farm/location` | Get location via IPGeolocation (proxy) |

### Advisory (AI)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/advisory/generate` | Generate RAG-grounded AI crop advisory |
| `POST` | `/api/advisory/chat` | Chat with multilingual AI farm assistant |
| `GET` | `/api/advisory/history/{farm_id}` | Get advisory history for a farm |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/admin/login` | Admin login |
| `GET` | `/api/admin/farmers` | List all farmers |
| `GET` | `/api/admin/advisories` | List all advisories |
| `GET` | `/api/admin/alerts` | List all alerts |
| `GET` | `/api/admin/analytics` | Platform analytics |

### Infrastructure
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check — service + DB + Redis status |

---

## 🌍 Supported Languages (AI Chat & Advisory)

`English` · `Hindi` · `Bengali` · `Telugu` · `Marathi` · `Tamil` · `Urdu` · `Gujarati` · `Kannada` · `Odia` · `Punjabi` · `Malayalam` · `Assamese`

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request — CI must pass before merge

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

