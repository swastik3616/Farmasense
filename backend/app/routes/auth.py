from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from app.models.models import User
import random, string

auth_bp   = Blueprint("auth", __name__)
otp_store = {}  # Use Redis in production

def generate_otp():
    return "".join(random.choices(string.digits, k=6))

@auth_bp.route("/send-otp", methods=["POST"])
def send_otp():
    data   = request.get_json()
    mobile = data.get("mobile_number")
    if not mobile:
        return jsonify({"error": "Mobile number required"}), 400

    otp = generate_otp()
    otp_store[mobile] = otp
    print(f"[DEV] OTP for {mobile}: {otp}")  # Remove in production
    return jsonify({"message": "OTP sent successfully"}), 200


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data   = request.get_json()
    mobile = data.get("mobile_number")
    otp    = data.get("otp")
    name   = data.get("name", "Farmer")

    if otp_store.get(mobile) != otp:
        return jsonify({"error": "Invalid OTP"}), 401

    user = User.query.filter_by(mobile_number=mobile).first()
    if not user:
        user = User(mobile_number=mobile, name=name)
        db.session.add(user)
        db.session.commit()

    otp_store.pop(mobile, None)
    token = create_access_token(identity=str(user.id))

    return jsonify({
        "token"  : token,
        "user_id": user.id,
        "name"   : user.name,
    }), 200