from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from beanie import PydanticObjectId

from app.security import (
    ai_rate_limit,
    sanitize_user_input,
    validate_language,
    validate_advisory_output,
)
from app.models.documents import Farm, Advisory, AdvisoryReport

advisory_bp = Blueprint("advisory", __name__)


@advisory_bp.route("/generate", methods=["POST"])
@ai_rate_limit(max_per_minute=3)
@jwt_required()
async def generate():
    data     = request.get_json(force=True, silent=True) or {}
    farm_id  = data.get("farm_id", "")
    language = data.get("language", "English")

    language, lang_err = validate_language(language)

    try:
        farm = await Farm.get(PydanticObjectId(farm_id))
    except Exception:
        return jsonify({"error": "Invalid farm ID format"}), 400

    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    farm_dict = {
        "id"              : str(farm.id),
        "latitude"        : farm.latitude,
        "longitude"       : farm.longitude,
        "district"        : farm.district,
        "state"           : farm.state,
        "soil_type"       : farm.soil_type,
        "soil_card_number": farm.soil_health_card_no,
        "land_size_acres" : farm.land_size_acres,
        "water_source"    : farm.water_source,
    }

    from app.agents.graph import farm_graph
    
    input_state = {
        "farm_dict": farm_dict,
        "language": language,
        "request_type": "advisory",
        "messages": [],
        "current_message": ""
    }
    
    output_state = farm_graph.invoke(input_state)
    raw_result = output_state.get("advisory_result", {})

    sanitized_result, warnings = validate_advisory_output(raw_result)
    if warnings:
        current_app.logger.warning(f"Advisory output warnings for farm {farm_id}: {warnings}")

    report = AdvisoryReport(
        farm_id=farm_id,
        result=sanitized_result,
        warnings=warnings,
        language=language
    )
    await report.insert()

    advisory = Advisory(
        farm_id=farm_id,
        season=sanitized_result.get("season"),
        report_id=str(report.id)
    )
    await advisory.insert()

    return jsonify({
        "advisory_id" : str(advisory.id),
        "season"      : sanitized_result.get("season"),
        "full_advisory": sanitized_result
    }), 200


@advisory_bp.route("/history/<farm_id>", methods=["GET"])
@jwt_required()
async def history(farm_id):
    try:
        PydanticObjectId(farm_id)
    except Exception:
        return jsonify({"error": "Invalid farm ID format"}), 400

    advisories = await Advisory.find(Advisory.farm_id == farm_id).sort("-created_at").to_list()

    result = []
    for a in advisories:
        result.append({
            "id"        : str(a.id),
            "season"    : a.season,
            "created_at": str(a.created_at),
        })

    return jsonify(result), 200


@advisory_bp.route("/chat", methods=["POST"])
@ai_rate_limit(max_per_minute=15)
@jwt_required()
async def chat():
    data    = request.get_json(force=True, silent=True) or {}
    farm_id = data.get("farm_id", "")
    message = data.get("message", "")
    language = data.get("language", "English")
    history = data.get("history", [])

    language, _ = validate_language(language)

    message, input_err = sanitize_user_input(message, max_length=500)
    if input_err:
        return jsonify({"error": input_err}), 400

    if not farm_id:
        return jsonify({"error": "Missing farm_id"}), 400

    safe_history = []
    for entry in history[:20]:
        role    = entry.get("role", "")
        content = entry.get("content", "")
        if role not in ("user", "ai"):
            continue
        clean_content, _ = sanitize_user_input(str(content), max_length=1000)
        safe_history.append({"role": role, "content": clean_content})

    try:
        farm = await Farm.get(PydanticObjectId(farm_id))
    except Exception:
        return jsonify({"error": "Invalid farm ID format"}), 400

    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    farm_dict = {
        "land_size_acres": farm.land_size_acres,
        "soil_type"      : farm.soil_type,
        "district"       : farm.district,
        "state"          : farm.state,
        "water_source"   : farm.water_source,
    }

    try:
        from app.agents.graph import farm_graph
        input_state = {
            "farm_dict": farm_dict,
            "language": language,
            "request_type": "chat",
            "messages": safe_history,
            "current_message": message
        }
        
        output_state = farm_graph.invoke(input_state)
        reply = output_state.get("chat_reply", "Timeout connecting to knowledge base.")

        import re
        reply = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", str(reply))

        return jsonify({"reply": reply}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500