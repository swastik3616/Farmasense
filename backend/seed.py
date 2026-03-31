from app import create_app
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

app = create_app()

with app.app_context():
    db = app.db
    print("Connecting to MongoDB Database...")
    
    # 0. DROP existing collections to ensure a clean slate
    print("Dropping existing collections...")
    for collection in ["users", "farms", "advisories", "alerts", "admins"]:
        db[collection].drop()
    
    print("Tables dropped. Seeding new mock data...")

    # 1. Create Admin
    admin_id = db["admins"].insert_one({
        "name": "Admin",
        "email": "admin@farmsense.com",
        "password": hash_password("admin123"),
        "created_at": datetime.utcnow()
    }).inserted_id
    print(f"Admin user created (admin@farmsense.com / admin123) with ID: {admin_id}")

    # 2. Add Dummy Farmers (Users)
    farmer1_id = db["users"].insert_one({
        "mobile_number": "9876543210", 
        "name": "Ramesh Kumar", 
        "language_preference": "hi",
        "created_at": datetime.utcnow()
    }).inserted_id
    
    farmer2_id = db["users"].insert_one({
        "mobile_number": "9123456780", 
        "name": "Suresh Patel", 
        "language_preference": "gu",
        "created_at": datetime.utcnow()
    }).inserted_id

    # 3. Add Dummy Farms
    farm1_id = db["farms"].insert_one({
        "user_id": str(farmer1_id), 
        "name": "North Field", 
        "latitude": 28.7, 
        "longitude": 77.1, 
        "land_size_acres": 5.5, 
        "water_source": "Borewell", 
        "soil_type": "Alluvial", 
        "district": "Karnal", 
        "state": "Haryana",
        "created_at": datetime.utcnow()
    }).inserted_id

    farm2_id = db["farms"].insert_one({
        "user_id": str(farmer2_id), 
        "name": "Mango Orchard", 
        "latitude": 21.1, 
        "longitude": 72.8, 
        "land_size_acres": 12.0, 
        "water_source": "Canal", 
        "soil_type": "Black Cotton", 
        "district": "Surat", 
        "state": "Gujarat",
        "created_at": datetime.utcnow()
    }).inserted_id

    # 4. Add Dummy Advisories
    db["advisories"].insert_many([
        {
            "farm_id": str(farm1_id), 
            "season": "Kharif", 
            "recommended_crop": "Rice", 
            "second_option_crop": "Maize", 
            "avoid_crop": "Cotton",
            "expected_profit_min": 45000, 
            "expected_profit_max": 60000, 
            "confidence_score": 0.88,
            "created_at": datetime.utcnow()
        },
        {
            "farm_id": str(farm2_id), 
            "season": "Rabi", 
            "recommended_crop": "Wheat", 
            "second_option_crop": "Mustard", 
            "avoid_crop": "Sugarcane",
            "expected_profit_min": 30000, 
            "expected_profit_max": 40000, 
            "confidence_score": 0.92,
            "created_at": datetime.utcnow()
        }
    ])

    # 5. Add Dummy Alerts
    db["alerts"].insert_many([
        {
            "farm_id": str(farm1_id), 
            "alert_type": "Weather", 
            "severity": "High", 
            "sent_via": "SMS",
            "message": "Heavy rainfall expected in next 48 hours. Delay pesticide application.",
            "created_at": datetime.utcnow()
        },
        {
            "farm_id": str(farm2_id), 
            "alert_type": "Market", 
            "severity": "Medium", 
            "sent_via": "WhatsApp",
            "message": "Wheat prices have surged by 15% in Surat APMC.",
            "created_at": datetime.utcnow()
        }
    ])

    print("Mock MongoDB Data successfully populated!")
