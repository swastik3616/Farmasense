from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required
import hashlib

admin_bp = Blueprint("admin", __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@admin_bp.route("/login", methods=["POST"])
def admin_login():
    data     = request.get_json()
    email    = data.get("email")
    password = data.get("password")
    
    admins = current_app.db["admins"]
    admin = admins.find_one({"email": email})

    if not admin or admin.get("password") != hash_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
        
    token = create_access_token(
        identity=str(admin["_id"]),
        additional_claims={"role": "admin"}
    )
    return jsonify({
        "token": token, 
        "name": admin.get("name"), 
        "email": admin.get("email"), 
        "role": "admin"
    }), 200


@admin_bp.route("/setup", methods=["POST"])
def setup_admin():
    admins = current_app.db["admins"]

    if admins.find_one():
        return jsonify({"error": "Admin already exists"}), 400
        
    data = request.get_json()
    
    from datetime import datetime
    admins.insert_one({
        "name": data.get("name", "Admin"),
        "email": data.get("email"),
        "password": hash_password(data.get("password")),
        "created_at": datetime.utcnow()
    })

    return jsonify({"message": "Admin created successfully"}), 201


@admin_bp.route("/farmers", methods=["GET"])
@jwt_required()
def get_farmers():
    users = current_app.db["users"]
    farms = current_app.db["farms"]
    
    # Sort by created_at descending if it exists, otherwise just fetch
    all_users = list(users.find().sort("created_at", -1))
    
    result = []
    for u in all_users:
        user_id_str = str(u["_id"])
        farms_count = farms.count_documents({"user_id": user_id_str})
        
        result.append({
            "id"         : user_id_str,
            "name"       : u.get("name"),
            "mobile"     : u.get("mobile_number"),
            "language"   : u.get("language_preference", "en"),
            "farms_count": farms_count,
            "created_at" : str(u.get("created_at", "N/A"))
        })

    return jsonify(result), 200


@admin_bp.route("/advisories", methods=["GET"])
@jwt_required()
def get_advisories():
    advisories_col = current_app.db["advisories"]
    
    advisories = list(advisories_col.find().sort("created_at", -1).limit(50))
    result = []
    
    for a in advisories:
        result.append({
            "id"              : str(a["_id"]),
            "farm_id"         : str(a.get("farm_id")),
            "recommended_crop": a.get("recommended_crop"),
            "season"          : a.get("season"),
            "created_at"      : str(a.get("created_at", "N/A")),
        })

    return jsonify(result), 200


@admin_bp.route("/analytics", methods=["GET"])
@jwt_required()
def get_analytics():
    db = current_app.db
    return jsonify({
        "total_farmers"   : db["users"].count_documents({}),
        "total_farms"     : db["farms"].count_documents({}),
        "total_advisories": db["advisories"].count_documents({}),
        "total_alerts"    : db["alerts"].count_documents({}),
    }), 200
