from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime
from bson import ObjectId

from app.security import (
    ai_rate_limit,
    sanitize_user_input,
    validate_language,
    validate_advisory_output,
)

advisory_bp = Blueprint("advisory", __name__)


@advisory_bp.route("/generate", methods=["POST"])
@jwt_required()
@ai_rate_limit(max_per_minute=3)   # max 3 advisory generations per user per minute
def generate():
    data     = request.get_json(force=True, silent=True) or {}
    farm_id  = data.get("farm_id", "")
    language = data.get("language", "English")

    # ── Validate language ──────────────────────────────────────
    language, lang_err = validate_language(language)
    # lang_err is non-fatal — we just silently fall back to English

    db = current_app.db

    try:
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

    # ── Call LangGraph Advisory Node ───────────────────────────
    from app.agents.graph import farm_graph
    
    input_state = {
        "farm_dict": farm_dict,
        "language": language,
        "request_type": "advisory",
        "messages": [],
        "current_message": ""
    }
    
    # Run the state machine
    output_state = farm_graph.invoke(input_state)
    raw_result = output_state.get("advisory_result", {})

    # ── Validate & sanitize LLM output before storage ──────────
    sanitized_result, warnings = validate_advisory_output(raw_result)
    if warnings:
        current_app.logger.warning(f"Advisory output warnings for farm {farm_id}: {warnings}")

    # ── Persist to MongoDB ─────────────────────────────────────
    report = db["advisory_reports"].insert_one({
        "farm_id"   : farm_id,
        "result"    : sanitized_result,
        "warnings"  : warnings,
        "language"  : language,
        "created_at": datetime.utcnow(),
    })

    advisory = db["advisories"].insert_one({
        "farm_id"   : farm_id,
        "season"    : sanitized_result.get("season"),
        "report_id" : str(report.inserted_id),
        "created_at": datetime.utcnow(),
    })

    return jsonify({
        "advisory_id" : str(advisory.inserted_id),
        "season"      : sanitized_result.get("season"),
        "full_advisory": sanitized_result
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
@ai_rate_limit(max_per_minute=15)  # chat is more interactive — 15 msgs/min per user
def chat():
    data    = request.get_json(force=True, silent=True) or {}
    farm_id = data.get("farm_id", "")
    message = data.get("message", "")
    language = data.get("language", "English")
    history = data.get("history", [])

    # ── Validate language ──────────────────────────────────────
    language, _ = validate_language(language)

    # ── Sanitize user message ──────────────────────────────────
    message, input_err = sanitize_user_input(message, max_length=500)
    if input_err:
        return jsonify({"error": input_err}), 400

    if not farm_id:
        return jsonify({"error": "Missing farm_id"}), 400

    # ── Sanitize chat history (prevent injection via history) ──
    safe_history = []
    for entry in history[:20]:   # cap history depth at 20 messages
        role    = entry.get("role", "")
        content = entry.get("content", "")
        if role not in ("user", "ai"):
            continue
        clean_content, _ = sanitize_user_input(str(content), max_length=1000)
        safe_history.append({"role": role, "content": clean_content})

    db = current_app.db
    try:
        farm = db["farms"].find_one({"_id": ObjectId(farm_id)})
    except Exception:
        return jsonify({"error": "Invalid farm ID format"}), 400

    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    farm_dict = {
        "land_size_acres": farm.get("land_size_acres"),
        "soil_type"      : farm.get("soil_type"),
        "district"       : farm.get("district"),
        "state"          : farm.get("state"),
        "water_source"   : farm.get("water_source"),
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

        # ── Basic output sanitization (strip control chars) ────
        import re
        reply = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", str(reply))

        return jsonify({"reply": reply}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500