from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
import hashlib

admin_bp = Blueprint("admin", __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@admin_bp.route("/login", methods=["POST"])
def admin_login():
    from app import db
    from app.models.models import Admin
    data     = request.get_json()
    email    = data.get("email")
    password = data.get("password")
    admin = Admin.query.filter_by(email=email).first()
    if not admin or admin.password != hash_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    token = create_access_token(
        identity=str(admin.id),
        additional_claims={"role": "admin"}
    )
    return jsonify({"token": token, "name": admin.name, "email": admin.email, "role": "admin"}), 200


@admin_bp.route("/setup", methods=["POST"])
def setup_admin():
    from app import db
    from app.models.models import Admin
    if Admin.query.first():
        return jsonify({"error": "Admin already exists"}), 400
    data  = request.get_json()
    admin = Admin(
        name     = data.get("name", "Admin"),
        email    = data.get("email"),
        password = hash_password(data.get("password"))
    )
    db.session.add(admin)
    db.session.commit()
    return jsonify({"message": "Admin created successfully"}), 201


@admin_bp.route("/farmers", methods=["GET"])
@jwt_required()
def get_farmers():
    from app.models.models import User
    farmers = User.query.order_by(User.created_at.desc()).all()
    return jsonify([{
        "id"        : f.id,
        "name"      : f.name,
        "mobile"    : f.mobile_number,
        "language"  : f.language_preference,
        "farms_count": len(f.farms),
        "created_at": str(f.created_at),
    } for f in farmers]), 200


@admin_bp.route("/advisories", methods=["GET"])
@jwt_required()
def get_advisories():
    from app.models.models import Advisory
    advisories = Advisory.query.order_by(Advisory.created_at.desc()).limit(50).all()
    return jsonify([{
        "id"              : a.id,
        "farm_id"         : a.farm_id,
        "recommended_crop": a.recommended_crop,
        "season"          : a.season,
        "created_at"      : str(a.created_at),
    } for a in advisories]), 200


@admin_bp.route("/analytics", methods=["GET"])
@jwt_required()
def get_analytics():
    from app.models.models import User, Farm, Advisory, Alert
    return jsonify({
        "total_farmers"   : User.query.count(),
        "total_farms"     : Farm.query.count(),
        "total_advisories": Advisory.query.count(),
        "total_alerts"    : Alert.query.count(),
    }), 200
