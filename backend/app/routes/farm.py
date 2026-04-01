from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
import os
import requests

farm_bp = Blueprint("farm", __name__)

@farm_bp.route("/location", methods=["GET"])
@jwt_required()
def get_location():
    api_key = os.getenv("Geolocation_ID")
    if not api_key:
        return jsonify({"error": "Geolocation API key not configured in backend .env"}), 500
    
    try:
        # Optionally pass IP, but omitting it will default to public IP
        response = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}")
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Failed to fetch from IPGeolocation API"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@farm_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_farms():
    db = current_app.db
    user_id = get_jwt_identity()
    
    try:
        user_farms_cursor = db["farms"].find({"user_id": str(user_id)})
        farms = []
        for farm in user_farms_cursor:
            farms.append({
                "id"             : str(farm["_id"]),
                "name"           : farm.get("name"),
                "latitude"       : farm.get("latitude"),
                "longitude"      : farm.get("longitude"),
                "land_size_acres": farm.get("land_size_acres"),
                "water_source"   : farm.get("water_source"),
                "soil_type"      : farm.get("soil_type"),
                "district"       : farm.get("district"),
                "state"          : farm.get("state"),
            })
        return jsonify(farms), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch farms", "details": str(e)}), 500


@farm_bp.route("/create", methods=["POST"])
@jwt_required()
def create_farm():
    db = current_app.db
    user_id = get_jwt_identity()
    data = request.get_json()

    farm = db["farms"].insert_one({
        "user_id"        : user_id,
        "name"           : data.get("name", "My Farm"),
        "latitude"       : data.get("latitude"),
        "longitude"      : data.get("longitude"),
        "land_size_acres": data.get("land_size_acres"),
        "water_source"   : data.get("water_source"),
        "district"       : data.get("district"),
        "state"          : data.get("state"),
        "soil_type"      : data.get("soil_type"),
        "soil_health_card_no": data.get("soil_health_card_number"),
        "created_at"     : datetime.utcnow(),
    })

    return jsonify({
        "message": "Farm created",
        "farm_id": str(farm.inserted_id)
    }), 201


@farm_bp.route("/<farm_id>", methods=["GET"])
@jwt_required()
def get_farm(farm_id):
    db = current_app.db

    try:
        farm = db["farms"].find_one({"_id": ObjectId(farm_id)})
    except:
        return jsonify({"error": "Invalid farm ID"}), 400

    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    return jsonify({
        "id"             : str(farm["_id"]),
        "name"           : farm.get("name"),
        "latitude"       : farm.get("latitude"),
        "longitude"      : farm.get("longitude"),
        "land_size_acres": farm.get("land_size_acres"),
        "water_source"   : farm.get("water_source"),
        "soil_type"      : farm.get("soil_type"),
        "district"       : farm.get("district"),
        "state"          : farm.get("state"),
    }), 200


@farm_bp.route("/<farm_id>", methods=["PUT"])
@jwt_required()
def update_farm(farm_id):
    db = current_app.db
    data = request.get_json()

    try:
        result = db["farms"].update_one(
            {"_id": ObjectId(farm_id)},
            {"$set": {
                "name"           : data.get("name"),
                "land_size_acres": data.get("land_size_acres"),
                "water_source"   : data.get("water_source"),
            }}
        )
    except:
        return jsonify({"error": "Invalid farm ID"}), 400

    if result.matched_count == 0:
        return jsonify({"error": "Farm not found"}), 404

    return jsonify({"message": "Farm updated"}), 200