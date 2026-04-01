from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from beanie import PydanticObjectId
from app.models.documents import Farm, Alert, CommunityReport

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/<farm_id>", methods=["GET"])
@jwt_required()
async def get_alerts(farm_id):
    try:
        alerts = await Alert.find(Alert.farm_id == farm_id).sort("-created_at").limit(20).to_list()
    except Exception:
        return jsonify({"error": "Invalid farm ID format"}), 400

    result = []
    for a in alerts:
        result.append({
            "id"        : str(a.id),
            "type"      : a.alert_type,
            "message"   : a.message,
            "severity"  : a.severity,
            "created_at": str(a.created_at),
        })

    return jsonify(result), 200


@alerts_bp.route("/create", methods=["POST"])
@jwt_required()
async def create_alert():
    data = request.get_json()

    alert = Alert(
        farm_id=data.get("farm_id", ""),
        alert_type=data.get("alert_type", "Info"),
        message=data.get("message", ""),
        severity=data.get("severity", "medium"),
        sent_via=data.get("sent_via", "sms")
    )
    await alert.insert()

    if data.get("sent_via", "sms") == "sms":
        # We need the user's phone number. Normally, fetch from Farm linked User,
        # but defaulting to system TWILIO_PHONE_NUMBER per previous logic.
        import os
        farmer_phone = os.getenv("TWILIO_PHONE_NUMBER")
        
        from app.tasks.communications import dispatch_sms_alert
        dispatch_sms_alert.delay(
            phone_number=farmer_phone, 
            body=data.get("message"),
            context_dict={"alert_id": str(alert.id)}
        )

    return jsonify({
        "message": "Alert created",
        "alert_id": str(alert.id)
    }), 201


@alerts_bp.route("/community/report", methods=["POST"])
@jwt_required()
async def community_report():
    user_id = get_jwt_identity()
    data = request.get_json()

    report = CommunityReport(
        user_id=str(user_id),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        report_type=data.get("report_type", "General"),
        description=data.get("description", ""),
        verified=False
    )
    await report.insert()

    return jsonify({
        "message": "Report submitted",
        "report_id": str(report.id)
    }), 201


@alerts_bp.route("/community/nearby", methods=["GET"])
@jwt_required()
async def nearby_reports():
    reports = await CommunityReport.find(CommunityReport.verified == True).sort("-created_at").limit(10).to_list()

    result = []
    for r in reports:
        result.append({
            "id"         : str(r.id),
            "report_type": r.report_type,
            "description": r.description,
            "latitude"   : r.latitude,
            "longitude"  : r.longitude,
            "created_at" : str(r.created_at),
        })

    return jsonify(result), 200