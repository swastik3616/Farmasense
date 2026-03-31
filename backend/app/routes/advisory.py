from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime

advisory_bp = Blueprint("advisory", __name__)


@advisory_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate():
    data    = request.get_json()
    farm_id = data.get("farm_id")

    db = current_app.db

    # ✅ Get farm from MongoDB
    farm = db["farms"].find_one({"_id": farm_id})

    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    farm_dict = {
        "id"              : str(farm["_id"]),
        "latitude"        : farm.get("latitude"),
        "longitude"       : farm.get("longitude"),
        "district"        : farm.get("district"),
        "state"           : farm.get("state"),
        "soil_type"       : farm.get("soil_type"),
        "soil_card_number": farm.get("soil_health_card_no"),
        "land_size_acres" : farm.get("land_size_acres"),
        "water_source"    : farm.get("water_source"),
    }

    # Import here to avoid circular imports
    from app.agents.orchestrator import generate_advisory
    result = generate_advisory(farm_dict)

    # ✅ Save full report in Mongo
    report = db["advisory_reports"].insert_one({
        "farm_id"   : farm_id,
        "result"    : result,
        "created_at": datetime.utcnow(),
    })

    # ✅ Save summary (also Mongo now)
    advisory = db["advisories"].insert_one({
        "farm_id"        : farm_id,
        "season"         : result.get("season"),
        "report_id"      : str(report.inserted_id),
        "created_at"     : datetime.utcnow(),
    })

    return jsonify({
        "advisory_id"   : str(advisory.inserted_id),
        "season"        : result.get("season"),
        "final_advisory": result.get("final_advisory"),
    }), 200


@advisory_bp.route("/history/<farm_id>", methods=["GET"])
@jwt_required()
def history(farm_id):
    db = current_app.db

    advisories = db["advisories"].find({"farm_id": farm_id})\
                                .sort("created_at", -1)

    result = []
    for a in advisories:
        result.append({
            "id"        : str(a["_id"]),
            "season"    : a.get("season"),
            "created_at": str(a.get("created_at")),
        })

    return jsonify(result), 200