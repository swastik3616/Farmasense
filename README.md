# FarmaSense 🌱

<div align="center">

![FarmaSense Banner](https://img.shields.io/badge/FarmaSense-Intelligent%20Agriculture-2ECC71?style=for-the-badge&logo=leaf&logoColor=white)

[![React](https://img.shields.io/badge/React-19.x-61DAFB?style=flat-square&logo=react)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb)](https://www.mongodb.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Groq-FF6B35?style=flat-square)](https://python.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

**An AI-powered agricultural intelligence platform designed to empower Indian farmers with smart crop advisories, real-time alerts, and a multilingual AI assistant.**

[Farmer Portal](#farmer-portal) · [Admin Dashboard](#admin-dashboard) · [API Docs](#api-endpoints) · [Getting Started](#getting-started)

</div>

---

## 📖 Overview

FarmaSense bridges the gap between modern AI and traditional farming. Farmers can register their farms, get AI-generated crop recommendations, receive weather & market alerts, and converse with an intelligent agricultural assistant — all in their **native Indian language**, right from their mobile phone.

---

## ✨ Features

### 🧑‍🌾 Farmer Portal
- **OTP-Based Authentication** — Secure mobile number login, no password required
- **Farm Registration** — Add farms with auto-location via IPGeolocation API
- **AI Crop Advisory** — LangChain + Groq-powered recommendations tailored to soil, district, season, and land size
- **Multilingual AI Chat** — Converse with the farm assistant in 13 Indian languages (Hindi, Marathi, Gujarati, Tamil, Telugu, and more)
- **Mobile-First Design** — Glassmorphism UI with bottom navigation bar optimized for smartphones

### 🛡️ Admin Dashboard
- **Secure Admin Login** — JWT-protected admin portal
- **Farmer Management** — View all registered farmers
- **Advisory Overview** — Monitor all AI-generated advisories
- **Alert Management** — View & manage system alerts
- **Platform Analytics** — Visual insights with Recharts

### 🔧 Platform Infrastructure
- **RESTful API** — Flask backend with well-organized Blueprint routes
- **JWT Authentication** — Stateless secure token-based auth for both farmers and admins
- **MongoDB** — Flexible NoSQL database for all collections
- **Task Scheduling** — APScheduler for automated background jobs
- **SMS Alerts** — Twilio integration for critical farm notifications

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js 19, React Router v7, Axios |
| **Styling** | Vanilla CSS (mobile-first, glassmorphism) |
| **Maps** | Leaflet + React-Leaflet |
| **Charts** | Recharts |
| **Backend** | Python 3.9+, Flask 3.0 |
| **Database** | MongoDB (pymongo) |
| **AI / LLM** | LangChain, ChatGroq (`llama-3.1-8b-instant`) |
| **Authentication** | Flask-JWT-Extended |
| **Geolocation** | IPGeolocation.io API |
| **Notifications** | Twilio (SMS/WhatsApp) |
| **Scheduling** | APScheduler |

---

## 🗂️ Project Structure

```
farmasense/
│
├── frontend/                    # React Application
│   ├── public/
│   └── src/
│       ├── components/
│       │   ├── AdminLayout.js   # Admin navigation wrapper
│       │   └── FarmerLayout.js  # Farmer bottom nav (mobile-first)
│       ├── context/
│       │   └── AuthContext.js   # Global auth state (farmer + admin)
│       ├── pages/
│       │   ├── admin/           # Admin portal pages
│       │   │   ├── AdminLogin.js
│       │   │   ├── Dashboard.js
│       │   │   ├── Farmers.js
│       │   │   ├── Advisories.js
│       │   │   ├── Alerts.js
│       │   │   └── Analytics.js
│       │   └── farmer/          # Farmer portal pages
│       │       ├── Login.js     # Mobile OTP login
│       │       ├── FarmerDashboard.js
│       │       ├── MyFarms.js
│       │       ├── AddFarm.js   # Farm registration + GPSLocation
│       │       └── FarmDetails.js  # AI advisory + multilingual chat
│       └── services/
│           └── api.js           # Centralized Axios API client
│
└── backend/                     # Flask REST API
    ├── app/
    │   ├── agents/
    │   │   └── orchestrator.py  # LangChain AI logic (advisory + chat)
    │   ├── models/
    │   │   └── models.py        # SQLAlchemy models (legacy reference)
    │   ├── routes/
    │   │   ├── auth.py          # OTP send/verify endpoints
    │   │   ├── farm.py          # Farm CRUD + geolocation proxy
    │   │   ├── advisory.py      # AI advisory generation + chat
    │   │   ├── alerts.py        # Alerts management
    │   │   ├── market.py        # Mandi price API
    │   │   └── admin.py         # Admin-only protected routes
    │   └── __init__.py          # App factory + MongoDB init
    ├── seed.py                  # MongoDB seed script (mock data)
    ├── .env                     # Environment variables (not committed)
    ├── requirements.txt
    └── run.py                   # App entry point
```

---

## 🗄️ MongoDB Collections

| Collection | Description |
|---|---|
| `admins` | Admin credentials (hashed passwords) |
| `users` | Farmer profiles (mobile, name, language preference) |
| `farms` | Farm details (location, soil, size, water source) |
| `advisories` | AI-generated crop recommendation summaries |
| `advisory_reports` | Full AI advisory JSON payloads |
| `alerts` | Weather/market alerts sent to farmers |

---

## 🚀 Getting Started

### Prerequisites

Ensure the following are installed on your machine:

- [Node.js](https://nodejs.org/) (v18+)
- [Python](https://python.org/) (v3.9+)
- [MongoDB](https://www.mongodb.com/) (local or Atlas URI)
- [Git](https://git-scm.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/swastik3616/Farmasense.git
cd Farmasense
```

### 2. Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` directory:

```env
# Flask
SECRET_KEY=your_secret_key
FLASK_ENV=development

# MongoDB
MONGO_URI=mongodb://localhost:27017/farmsense

# Groq AI
GROQ_API_KEY=your_groq_api_key

# IPGeolocation
Geolocation_ID=your_ipgeolocation_api_key

# Twilio (Optional)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx

# WeatherMap (Optional)
WEATHER_API_KEY=your_openweathermap_key
```

Seed the database with mock data (optional):

```bash
python seed.py
```

Start the backend server:

```bash
python run.py
```

> The API will be accessible at `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

> The app will open at `http://localhost:3000`

---

## 🌐 Accessing the Portals

| Portal | URL | Credentials |
|--------|-----|-------------|
| **Farmer Portal** | `http://localhost:3000/farmer/login` | Any 10-digit mobile + OTP (check backend console) |
| **Admin Dashboard** | `http://localhost:3000/admin/login` | `admin@farmsense.com` / `admin123` |

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
| `GET` | `/api/farm/<id>` | Get a specific farm |
| `GET` | `/api/farm/location` | Get location via IPGeolocation (proxy) |

### Advisory (AI)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/advisory/generate` | Generate AI crop advisory |
| `POST` | `/api/advisory/chat` | Chat with AI farm assistant |
| `GET` | `/api/advisory/history/<farm_id>` | Get advisory history |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/admin/login` | Admin login |
| `GET` | `/api/admin/farmers` | List all farmers |
| `GET` | `/api/admin/advisories` | List all advisories |
| `GET` | `/api/admin/alerts` | List all alerts |
| `GET` | `/api/admin/analytics` | Platform analytics |

---

## 🌍 Supported Languages (AI Chat & Advisory)

The AI assistant supports responses in the following Indian languages:

`English` · `Hindi` · `Bengali` · `Telugu` · `Marathi` · `Tamil` · `Urdu` · `Gujarati` · `Kannada` · `Odia` · `Punjabi` · `Malayalam` · `Assamese`

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ for Indian Farmers · Powered by AI
</div>
