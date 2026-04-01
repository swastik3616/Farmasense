from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import requests
from beanie import PydanticObjectId
from app.models.documents import Farm

farm_bp = Blueprint("farm", __name__)

@farm_bp.route("/location", methods=["GET"])
@jwt_required()
def get_location():
    api_key = os.getenv("Geolocation_ID")
    if not api_key:
        return jsonify({"error": "Geolocation API key not configured in backend .env"}), 500
    
    try:
        response = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}")
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Failed to fetch from IPGeolocation API"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@farm_bp.route("/", methods=["GET"])
@jwt_required()
async def get_user_farms():
    user_id = get_jwt_identity()
    
    try:
        user_farms = await Farm.find(Farm.user_id == str(user_id)).to_list()
        farms = []
        for farm in user_farms:
            farms.append({
                "id"             : str(farm.id),
                "name"           : farm.name,
                "latitude"       : farm.latitude,
                "longitude"      : farm.longitude,
                "land_size_acres": farm.land_size_acres,
                "water_source"   : farm.water_source,
                "soil_type"      : farm.soil_type,
                "district"       : farm.district,
                "state"          : farm.state,
            })
        return jsonify(farms), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch farms", "details": str(e)}), 500


@farm_bp.route("/create", methods=["POST"])
@jwt_required()
async def create_farm():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Beanie naturally validates datatypes like floats and strings based on document schema
    try:
        farm = Farm(
            user_id=str(user_id),
            name=data.get("name", "My Farm"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            land_size_acres=data.get("land_size_acres"),
            water_source=data.get("water_source"),
            district=data.get("district"),
            state=data.get("state"),
            soil_type=data.get("soil_type"),
            soil_health_card_no=data.get("soil_health_card_number")
        )
        await farm.insert()

        return jsonify({
            "message": "Farm created",
            "farm_id": str(farm.id)
        }), 201
    except ValueError as e:
        # Pydantic validation error catch
        return jsonify({"error": "Invalid data format provided", "details": str(e)}), 422


@farm_bp.route("/<farm_id>", methods=["GET"])
@jwt_required()
async def get_farm(farm_id):
    try:
        farm = await Farm.get(PydanticObjectId(farm_id))
    except Exception:
        return jsonify({"error": "Invalid farm ID format"}), 400

    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    return jsonify({
        "id"             : str(farm.id),
        "name"           : farm.name,
        "latitude"       : farm.latitude,
        "longitude"      : farm.longitude,
        "land_size_acres": farm.land_size_acres,
        "water_source"   : farm.water_source,
        "soil_type"      : farm.soil_type,
        "district"       : farm.district,
        "state"          : farm.state,
    }), 200


@farm_bp.route("/<farm_id>", methods=["PUT"])
@jwt_required()
async def update_farm(farm_id):
    data = request.get_json()

    try:
        farm = await Farm.get(PydanticObjectId(farm_id))
    except Exception:
        return jsonify({"error": "Invalid farm ID format"}), 400

    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    try:
        # Only update fields that are provided
        if "name" in data:
            farm.name = data["name"]
        if "land_size_acres" in data:
            farm.land_size_acres = data["land_size_acres"]
        if "water_source" in data:
            farm.water_source = data["water_source"]
            
        await farm.save()
        return jsonify({"message": "Farm updated"}), 200
        
    except ValueError as e:
        return jsonify({"error": "Invalid data type", "details": str(e)}), 422