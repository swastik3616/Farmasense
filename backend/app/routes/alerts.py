from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import Alert, CommunityReport

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/<int:farm_id>", methods=["GET"])
@jwt_required()
def get_alerts(farm_id):
    alerts = Alert.query.filter_by(farm_id=farm_id)\
                        .order_by(Alert.created_at.desc()).limit(20).all()
    return jsonify([{
        "id"        : a.id,
        "type"      : a.alert_type,
        "message"   : a.message,
        "severity"  : a.severity,
        "created_at": str(a.created_at),
    } for a in alerts]), 200


@alerts_bp.route("/create", methods=["POST"])
@jwt_required()
def create_alert():
    data  = request.get_json()
    alert = Alert(
        farm_id    = data["farm_id"],
        alert_type = data["alert_type"],
        message    = data["message"],
        severity   = data.get("severity", "medium"),
        sent_via   = data.get("sent_via", "sms"),
    )
    db.session.add(alert)
    db.session.commit()
    return jsonify({"message": "Alert created", "alert_id": alert.id}), 201


@alerts_bp.route("/community/report", methods=["POST"])
@jwt_required()
def community_report():
    user_id = int(get_jwt_identity())
    data    = request.get_json()
    report  = CommunityReport(
        user_id     = user_id,
        latitude    = data.get("latitude"),
        longitude   = data.get("longitude"),
        report_type = data.get("report_type"),
        description = data.get("description"),
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({"message": "Report submitted", "report_id": report.id}), 201


@alerts_bp.route("/community/nearby", methods=["GET"])
@jwt_required()
def nearby_reports():
    reports = CommunityReport.query.filter_by(verified=True)\
                             .order_by(CommunityReport.created_at.desc()).limit(10).all()
    return jsonify([{
        "id"         : r.id,
        "report_type": r.report_type,
        "description": r.description,
        "latitude"   : r.latitude,
        "longitude"  : r.longitude,
        "created_at" : str(r.created_at),
    } for r in reports]), 200