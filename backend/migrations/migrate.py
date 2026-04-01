import sys
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.documents import User, Admin, Farm, Advisory, AdvisoryReport, Alert, CommunityReport, DLQSms

async def run_migrations():
    """
    Core Beanie Migration Execution Point.
    We connect to the db, load the documents, and optionally run custom sync scripts here.
    """
    print("Initiating Beanie ODM Migration Pipeline...")
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/farmsense")
    client = AsyncIOMotorClient(uri)
    db = client.get_default_database()
    
    # Init Beanie simply forces indices to be built automatically.
    print("Building and enforcing indexes constraints based on Document Settings...")
    await init_beanie(database=db, document_models=[
        User, Admin, Farm, Advisory, AdvisoryReport, Alert, CommunityReport, DLQSms
    ])
    
    print("✅ Indexes enforced via ODM successfully.")
    
    # -------------------------------------------------------------
    # Example Migration: Convert older string fields to numbers, etc.
    # -------------------------------------------------------------
    
    # Example:
    # print("Patching legacy farm land_sizes...")
    # async for farm in Farm.find(Farm.land_size_acres == None):
    #     if hasattr(farm, "legacy_size"):
    #         farm.land_size_acres = float(farm.legacy_size)
    #         await farm.save()
    
    print("No custom data transformations queued.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    
    asyncio.run(run_migrations())
