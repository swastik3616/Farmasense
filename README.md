# FarmaSense

FarmaSense is an intelligent agricultural platform designed to assist farmers and agricultural stakeholders with tools for farm management, market tracking, real-time alerts, and AI-driven advisory services. Built with a modern tech stack encompassing a React frontend and a Flask backend, the system leverages Generative AI (Groq, Gemini), Twilio for notifications, and interactive mapping via Leaflet.

## Features

- **Farm Management:** Easily track, record, and manage farm-related data.
- **AI Advisory:** Get intelligent, context-aware agricultural advice powered by LangChain and Generative AI (Google Generative AI, Groq).
- **Market Insights:** Real-time access to agricultural market rates and data.
- **Alerts & Notifications:** Receive timely SMS alerts about critical farming conditions, weather, or market shifts utilizing Twilio.
- **Admin Dashboard:** Centralized admin portal for comprehensive platform management.
- **Interactive Maps:** Visualize farm locations and geographic data seamlessly using React Leaflet.

## Tech Stack

### Frontend
- **Framework:** React.js
- **Routing:** React Router DOM
- **Maps:** Leaflet & React-Leaflet
- **Charts:** Recharts
- **HTTP Client:** Axios

### Backend
- **Framework:** Python, Flask
- **Databases:** 
  - Relational: SQL (PyODBC, SQLAlchemy)
  - Key-Value / Caching: Redis
- **Authentication:** Flask-JWT-Extended
- **AI Integration:** LangChain, LangGraph, Google Generative AI, Langchain-Groq
- **Task Scheduling:** APScheduler
- **Communications:** Twilio (SMS/Alerts)
- **Image Processing:** Pillow

## Project Structure

```text
farmasense/
│
├── frontend/             # React Application
│   ├── public/           # Static assets
│   ├── src/              # React components and configurations
│   └── package.json      # Node dependencies and scripts
│
└── backend/              # Flask API Application
    ├── app/
    │   ├── agents/       # AI & LangChain agent logic
    │   ├── models/       # Database models & schemas
    │   ├── routes/       # API endpoints (Auth, Farm, Advisory, Market, Alerts, Admin)
    │   ├── services/     # Business logic & 3rd party integrations
    │   └── utils/        # Utility helpers
    ├── .env              # Environment variables
    ├── requirements.txt  # Python package dependencies
    └── run.py            # Entry point for backend server
```

## Getting Started

### Prerequisites

Ensure you have the following installed on your machine:
- Node.js (v16+)
- Python (v3.9+)
- Redis Server
- T-SQL Server

### Setting up the Backend

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual Python environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file mimicking any required environment variables (e.g., Database URIs, Twilio credentials, API keys for Groq/Gemini).
5. Start the REST API server:
   ```bash
   python run.py
   ```

### Setting up the Frontend

1. Open a new terminal instance and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the necessary Node modules:
   ```bash
   npm install
   ```
3. Start the React development server (typically runs on `http://localhost:3000`):
   ```bash
   npm start
   ```

### Accessing the Portals

Once both the frontend and backend servers are running, you can access the application in your browser:

- **Farmer Portal**: `http://localhost:3000/farmer/login` *(Default Root)*
- **Admin Dashboard**: `http://localhost:3000/admin/login`

## License
This project is licensed under the [MIT License](LICENSE).
