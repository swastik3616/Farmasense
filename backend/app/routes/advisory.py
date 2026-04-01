from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime

advisory_bp = Blueprint("advisory", __name__)


@advisory_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate():
    data    = request.get_json()
    farm_id = data.get("farm_id")
    language = data.get("language", "English")

    db = current_app.db
    
    from bson import ObjectId
    try:
        # ✅ Get farm from MongoDB
        farm = db["farms"].find_one({"_id": ObjectId(farm_id)})
    except Exception:
        return jsonify({"error": "Invalid farm ID format"}), 400

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
    result = generate_advisory(farm_dict, language=language)

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
        "full_advisory" : result
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


@advisory_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    data    = request.get_json()
    farm_id = data.get("farm_id")
    message = data.get("message")
    language = data.get("language", "English")
    history = data.get("history", [])

    if not farm_id or not message:
        return jsonify({"error": "Missing farm_id or message"}), 400

    from bson import ObjectId
    db = current_app.db
    
    try:
        farm = db["farms"].find_one({"_id": ObjectId(farm_id)})
    except Exception:
        return jsonify({"error": "Invalid farm ID format"}), 400

    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    farm_dict = {
        "land_size_acres" : farm.get("land_size_acres"),
        "soil_type"       : farm.get("soil_type"),
        "district"        : farm.get("district"),
        "state"           : farm.get("state"),
        "water_source"    : farm.get("water_source"),
    }

    try:
        from app.agents.orchestrator import chat_with_advisory
        reply = chat_with_advisory(
            farm_dict=farm_dict, 
            history=history, 
            message=message, 
            language=language
        )
        return jsonify({"reply": reply}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500