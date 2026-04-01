import motor.motor_asyncio
from beanie import init_beanie
from app.models.documents import (
    User, Admin, Farm, Advisory, AdvisoryReport, 
    Alert, CommunityReport, DLQSms
)

async def init_db(app):
    """
    Initializes the asynchronous Motor client and configures Beanie ODM with all document models.
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(app.config["MONGO_URI"])
    db = client["farmsense"]
    
    await init_beanie(database=db, document_models=[
        User, Admin, Farm, Advisory, AdvisoryReport, 
        Alert, CommunityReport, DLQSms
    ])
    
    # Optional: Attach db to app for manual operations if absolutely required
    app.db = db
