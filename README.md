# FarmaSense 🌱

<div align="center">

![FarmaSense Banner](https://img.shields.io/badge/FarmaSense-Intelligent%20Agriculture-2ECC71?style=for-the-badge&logo=leaf&logoColor=white)

[![React](https://img.shields.io/badge/React-19.x-61DAFB?style=flat-square&logo=react)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb)](https://www.mongodb.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Groq-FF6B35?style=flat-square)](https://python.langchain.com/)
[![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=flat-square&logo=redis)](https://redis.io/)
[![CI](https://github.com/swastik3616/Farmasense/actions/workflows/ci.yml/badge.svg)](https://github.com/swastik3616/Farmasense/actions)
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
- **AI Crop Advisory** — LangGraph state machine + Groq-powered recommendations tailored to soil, district, season, and land size — grounded by RAG over a crop/soil knowledge base via MongoDB Atlas Vector Search
- **Multilingual AI Chat** — Converse with the farm assistant in 13 Indian languages (Hindi, Marathi, Gujarati, Tamil, Telugu, and more)
- **Mobile-First Design** — Glassmorphism UI with bottom navigation bar, loading skeletons, and clear error states optimised for smartphones

### 🛡️ Admin Dashboard
- **Secure Admin Login** — JWT-protected admin portal
- **Farmer Management** — View all registered farmers
- **Advisory Overview** — Monitor all AI-generated advisories
- **Alert Management** — View & manage system alerts
- **Platform Analytics** — Visual insights with Recharts

### 🔧 Platform Infrastructure
- **RESTful API** — Flask 3.0 backend with Blueprint route structure
- **JWT Authentication** — Stateless secure token-based auth for farmers and admins
- **MongoDB Atlas** — Async Beanie ODM with schema-enforced documents and Atlas Vector Search for RAG
- **Security Layer** — Per-endpoint AI rate limiting, prompt injection defense, and Pydantic output validation before every MongoDB write
- **SMS / WhatsApp Alerts** — Twilio integration with tenacity retry logic
- **CI/CD Pipeline** — GitHub Actions with flake8 lint, pytest, and 70% coverage gate on every merge

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js 19, React Router v7, Axios |
| **Styling** | Vanilla CSS (mobile-first, glassmorphism) |
| **Maps** | Leaflet + React-Leaflet |
| **Charts** | Recharts |
| **Backend** | Python 3.11, Flask 3.0 |
| **Database** | MongoDB Atlas — Beanie ODM (async) + Atlas Vector Search |
| **Caching** | Redis |
| **AI / LLM** | LangGraph state machine, LangChain, ChatGroq (`llama-3.1-8b-instant`) |
| **RAG** | MongoDB Atlas Vector Search + sentence-transformers embeddings |
| **Data Validation** | Pydantic v2 |
| **Authentication** | Flask-JWT-Extended |
| **Geolocation** | IPGeolocation.io API |
| **Notifications** | Twilio (SMS/WhatsApp) + tenacity retry |
| **Testing** | Pytest, pytest-asyncio, mongomock-motor, coverage |
| **CI/CD** | GitHub Actions |

---

## 🗂️ Project Structure

```
farmasense/
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # Lint, test, 70% coverage gate on every PR
│
├── frontend/                         # React Application
│   ├── public/
│   │   ├── manifest.json             # PWA manifest
│   │   ├── index.html
│   │   └── favicon.ico
│   └── src/
│       ├── components/
│       │   ├── AdminLayout.js        # Admin navigation wrapper
│       │   ├── FarmerLayout.js       # Farmer bottom nav (mobile-first)
│       │   └── Skeleton.js           # Loading skeleton components
│       ├── context/
│       │   └── AuthContext.js        # Global auth state (farmer + admin)
│       ├── pages/
│       │   ├── admin/
│       │   │   ├── AdminLogin.js
│       │   │   ├── Dashboard.js
│       │   │   ├── Farmers.js
│       │   │   ├── Advisories.js
│       │   │   ├── Alerts.js
│       │   │   └── Analytics.js
│       │   └── farmer/
│       │       ├── Login.js
│       │       ├── FarmerDashboard.js
│       │       ├── MyFarms.js
│       │       ├── AddFarm.js
│       │       └── FarmDetails.js
│       └── services/
│           └── api.js
│
└── backend/                          # Flask Application
    ├── app/
    │   ├── agents/
    │   │   ├── graph.py              # LangGraph state machine (RAG → advisory or chat)
    │   │   ├── state.py              # GraphState TypedDict
    │   │   ├── rag.py                # Atlas Vector Search retrieval
    │   │   └── nodes/
    │   │       ├── advisory.py       # Advisory generation node
    │   │       └── chat.py           # Multilingual chat node
    │   ├── models/
    │   │   └── documents.py          # Beanie ODM document definitions
    │   ├── routes/
    │   │   ├── auth.py               # OTP send/verify
    │   │   ├── farm.py               # Farm CRUD + geolocation proxy
    │   │   ├── advisory.py           # AI advisory + chat (rate limited, sanitized)
    │   │   ├── alerts.py             # Alerts management
    │   │   ├── market.py             # Mandi price API
    │   │   └── admin.py              # Admin-only routes
    │   ├── security.py               # Rate limiting, input sanitization, output validation
    │   └── __init__.py               # App factory + MongoDB + Beanie init
    ├── tests/
    │   ├── conftest.py               # Fixtures, mongomock-motor DB isolation
    │   ├── test_auth.py
    │   ├── test_advisory.py
    │   └── test_farm.py
    ├── seed.py
    ├── .env.example
    ├── requirements.txt
    ├── requirements-dev.txt
    └── run.py                        # Entry point — port 5000
```

---

## 🏗️ Architecture

### AI Pipeline (LangGraph)

```
POST /api/advisory/generate  or  POST /api/advisory/chat
     │
     ▼
Security layer
  ├── JWT auth (@jwt_required)
  ├── Rate limit (@ai_rate_limit — 3/min advisory, 15/min chat)
  └── Input sanitization (sanitize_user_input)
     │
     ▼
LangGraph state machine
  └── RAG retrieval node — Atlas Vector Search
         │
         ▼  conditional routing on request_type
    ┌────┴────┐
advisory    chat
  node       node
    └────┬────┘
         ▼
  Pydantic output validation (validate_advisory_output)
         │
         ▼
  Beanie async insert → MongoDB Atlas
```

---

## 🚀 Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) v18+
- [Python](https://python.org/) v3.11+
- [MongoDB Atlas](https://www.mongodb.com/) account (Vector Search required)
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
pip install -r requirements-dev.txt
```

```bash
cp .env.example .env
```

```env
SECRET_KEY=your_secret_key
FLASK_ENV=development

MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/farmasense
REDIS_URL=redis://localhost:6379/0

GROQ_API_KEY=your_groq_api_key
GEOLOCATION_API_KEY=your_ipgeolocation_api_key

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx

WEATHER_API_KEY=your_openweathermap_key
```

```bash
python seed.py
python run.py
```

> API at `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

> App at `http://localhost:3000`

### 4. Run Tests

```bash
cd backend
pytest tests/ --cov=app --cov-report=term-missing
```

---

## 🌐 Accessing the Portals

| Portal | URL |
|--------|-----|
| **Farmer Portal** | `http://localhost:3000/farmer/login` |
| **Admin Dashboard** | `http://localhost:3000/admin/login` |

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/send-otp` | Send OTP to farmer mobile |
| `POST` | `/api/auth/verify-otp` | Verify OTP and return JWT |

### Farm
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/farm/` | Get all farms for current user |
| `POST` | `/api/farm/create` | Register a new farm |
| `GET` | `/api/farm/<id>` | Get a specific farm |
| `GET` | `/api/farm/location` | Geolocation proxy |

### Advisory
| Method | Endpoint | Rate limit | Description |
|--------|----------|------------|-------------|
| `POST` | `/api/advisory/generate` | 3 / min | RAG-grounded crop advisory |
| `POST` | `/api/advisory/chat` | 15 / min | Multilingual AI chat |
| `GET` | `/api/advisory/history/<farm_id>` | — | Advisory history |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/admin/login` | Admin login |
| `GET` | `/api/admin/farmers` | List all farmers |
| `GET` | `/api/admin/advisories` | List all advisories |
| `GET` | `/api/admin/alerts` | List all alerts |
| `GET` | `/api/admin/analytics` | Platform analytics |

---

## 🗄️ MongoDB Collections

| Collection | Description |
|---|---|
| `users` | Farmer profiles |
| `admins` | Admin credentials (hashed) |
| `farms` | Farm details — indexed on `user_id` |
| `advisories` | Advisory summaries — indexed on `farm_id`, `created_at` |
| `advisory_reports` | Pydantic-validated full advisory payloads |
| `alerts` | Weather/market alerts — indexed on `user_id`, `created_at` |
| `community_reports` | Farmer field observations |
| `dlq_sms` | Dead letter queue for failed Twilio SMS |

---

## 🌍 Supported Languages

`English` · `Hindi` · `Bengali` · `Telugu` · `Marathi` · `Tamil` · `Urdu` · `Gujarati` · `Kannada` · `Odia` · `Punjabi` · `Malayalam` · `Assamese`

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit with a descriptive message: `git commit -m "feat: add X to solve Y"`
4. Push and open a pull request — CI must pass before merge

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

