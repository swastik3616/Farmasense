from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/<farm_id>", methods=["GET"])
@jwt_required()
def get_alerts(farm_id):
    db = current_app.db

    alerts = db["alerts"].find({"farm_id": farm_id})\
                         .sort("created_at", -1)\
                         .limit(20)

    result = []
    for a in alerts:
        result.append({
            "id"        : str(a["_id"]),
            "type"      : a.get("alert_type"),
            "message"   : a.get("message"),
            "severity"  : a.get("severity"),
            "created_at": str(a.get("created_at")),
        })

    return jsonify(result), 200


@alerts_bp.route("/create", methods=["POST"])
@jwt_required()
def create_alert():
    db = current_app.db
    data = request.get_json()

    alert = db["alerts"].insert_one({
        "farm_id"    : data.get("farm_id"),
        "alert_type" : data.get("alert_type"),
        "message"    : data.get("message"),
        "severity"   : data.get("severity", "medium"),
        "sent_via"   : data.get("sent_via", "sms"),
        "created_at" : datetime.utcnow(),
    })

    return jsonify({
        "message": "Alert created",
        "alert_id": str(alert.inserted_id)
    }), 201


@alerts_bp.route("/community/report", methods=["POST"])
@jwt_required()
def community_report():
    db = current_app.db
    user_id = get_jwt_identity()
    data = request.get_json()

    report = db["community_reports"].insert_one({
        "user_id"    : user_id,
        "latitude"   : data.get("latitude"),
        "longitude"  : data.get("longitude"),
        "report_type": data.get("report_type"),
        "description": data.get("description"),
        "verified"   : False,
        "created_at" : datetime.utcnow(),
    })

    return jsonify({
        "message": "Report submitted",
        "report_id": str(report.inserted_id)
    }), 201


@alerts_bp.route("/community/nearby", methods=["GET"])
@jwt_required()
def nearby_reports():
    db = current_app.db

    reports = db["community_reports"].find({"verified": True})\
                                     .sort("created_at", -1)\
                                     .limit(10)

    result = []
    for r in reports:
        result.append({
            "id"         : str(r["_id"]),
            "report_type": r.get("report_type"),
            "description": r.get("description"),
            "latitude"   : r.get("latitude"),
            "longitude"  : r.get("longitude"),
            "created_at" : str(r.get("created_at")),
        })

    return jsonify(result), 200