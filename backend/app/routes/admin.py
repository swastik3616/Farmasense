from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
import hashlib
from app.models.documents import Admin, User, Farm, Advisory, Alert

admin_bp = Blueprint("admin", __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@admin_bp.route("/login", methods=["POST"])
async def admin_login():
    data     = request.get_json()
    email    = data.get("email")
    password = data.get("password")
    
    admin = await Admin.find_one(Admin.email == email)

    if not admin or admin.password != hash_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
        
    token = create_access_token(
        identity=str(admin.id),
        additional_claims={"role": "admin"}
    )
    return jsonify({
        "token": token, 
        "name": "Admin", 
        "email": admin.email, 
        "role": "admin"
    }), 200


@admin_bp.route("/setup", methods=["POST"])
async def setup_admin():
    existing_admin = await Admin.find_one()

    if existing_admin:
        return jsonify({"error": "Admin already exists"}), 400
        
    data = request.get_json()
    
    admin = Admin(
        email=data.get("email"),
        password=hash_password(data.get("password"))
    )
    await admin.insert()

    return jsonify({"message": "Admin created successfully"}), 201


@admin_bp.route("/farmers", methods=["GET"])
@jwt_required()
async def get_farmers():
    # Sort by created_at descending
    all_users = await User.find_all().sort("-created_at").to_list()
    
    result = []
    for u in all_users:
        user_id_str = str(u.id)
        # async count of farms
        farms_count = await Farm.find(Farm.user_id == user_id_str).count()
        
        result.append({
            "id"         : user_id_str,
            "name"       : u.name,
            "mobile"     : u.mobile,
            "language"   : u.language,
            "farms_count": farms_count,
            "created_at" : str(u.created_at)
        })

    return jsonify(result), 200


@admin_bp.route("/advisories", methods=["GET"])
@jwt_required()
async def get_advisories():
    advisories = await Advisory.find_all().sort("-created_at").limit(50).to_list()
    result = []
    
    for a in advisories:
        result.append({
            "id"              : str(a.id),
            "farm_id"         : a.farm_id,
            "season"          : a.season,
            "created_at"      : str(a.created_at),
        })

    return jsonify(result), 200


@admin_bp.route("/alerts", methods=["GET"])
@jwt_required()
async def get_alerts():
    alerts = await Alert.find_all().sort("-created_at").limit(50).to_list()
    result = []
    
    for a in alerts:
        result.append({
            "id"        : str(a.id),
            "farm_id"   : a.farm_id,
            "alert_type": a.alert_type,
            "severity"  : a.severity,
            "message"   : a.message,
            "sent_via"  : a.sent_via,
            "created_at": str(a.created_at),
        })

    return jsonify(result), 200


@admin_bp.route("/analytics", methods=["GET"])
@jwt_required()
async def get_analytics():
    return jsonify({
        "total_farmers"   : await User.count(),
        "total_farms"     : await Farm.count(),
        "total_advisories": await Advisory.count(),
        "total_alerts"    : await Alert.count(),
    }), 200
