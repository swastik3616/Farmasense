import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY     = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # ❌ REMOVE SQL completely (no SQLALCHEMY)

    # MongoDB (Atlas)
    MONGO_URI = os.getenv("MONGO_URI")

    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Weather
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

    # Mandi
    MANDI_API_KEY = os.getenv("MANDI_API_KEY")

    # Twilio
    TWILIO_ACCOUNT_SID  = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN   = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")