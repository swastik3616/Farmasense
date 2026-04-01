import requests
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os
import asyncio
from app.models.documents import Farm, User, Alert
from app.tasks.communications import dispatch_sms_alert
from app.extensions import celery

async def check_weather_and_alert():
    """
    Async logic to fetch severe weather for all farms and trigger LLM alerts.
    """
    # 1. Init Beanie DB connection for script execution context
    client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/farmsense"))
    await init_beanie(database=client.get_default_database(), document_models=[Farm, User, Alert])

    farms = await Farm.find_all().to_list()
    
    for farm in farms:
        if not farm.latitude or not farm.longitude:
            continue
            
        print(f"[WEATHER] Checking weather for farm: {farm.id} at {farm.latitude}, {farm.longitude}")
        
        try:
            # Free weather API. Hits daily forecast for precipitation and max wind
            url = f"https://api.open-meteo.com/v1/forecast?latitude={farm.latitude}&longitude={farm.longitude}&daily=precipitation_sum,wind_speed_10m_max&timezone=auto"
            res = requests.get(url, timeout=10)
            data = res.json()
            
            daily = data.get("daily", {})
            if not daily:
                continue
                
            rain_mm = daily.get("precipitation_sum", [0])[0]
            wind_kmh = daily.get("wind_speed_10m_max", [0])[0]
            
            severe_event = None
            if rain_mm > 50:
                severe_event = f"Heavy Rain ({rain_mm}mm)"
            elif wind_kmh > 40:
                severe_event = f"Gale Winds ({wind_kmh}km/h)"
                
            if severe_event:
                print(f"[WEATHER] Severe event detected: {severe_event} for farm {farm.id}")
                
                # Fetch User for Language and Phone
                user = await User.get(farm.user_id)
                if not user:
                    continue
                
                # We could route this directly through LangGraph's advisory node with request_type: "alert" 
                # For immediate SMS dispatch reliability without blocking on AI API, we format a proactive skeleton.
                
                message = f"🚨 FarmaSense Weather Alert: {severe_event} expected tomorrow at your farm '{farm.name}'. Please secure crops and equipment. - AI Advisor"
                
                # Save Alert to DB
                alert = Alert(
                    farm_id=str(farm.id),
                    alert_type="Severe Weather",
                    message=message,
                    severity="high",
                    sent_via="sms"
                )
                await alert.insert()
                
                # Trigger SMS immediately via Twilio
                target_phone = user.mobile if user.mobile.startswith('+') else os.getenv("TWILIO_PHONE_NUMBER")
                dispatch_sms_alert.delay(phone_number=target_phone, body=message, context_dict={"alert_id": str(alert.id)})
                
        except Exception as e:
            print(f"Failed to check weather for farm {farm.id}: {e}")

@celery.task(name="tasks.monitor_farm_weather")
def monitor_farm_weather():
    """
    Synchronous Celery task wrapper that isolates the async event loop.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(check_weather_and_alert())
