from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.documents import User
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

    print(f"[DEV] OTP for {mobile}: {otp}")  # remove in production

    return jsonify({"message": "OTP sent successfully"}), 200


@auth_bp.route("/verify-otp", methods=["POST"])
async def verify_otp():
    data   = request.get_json()
    mobile = data.get("mobile_number")
    otp    = data.get("otp")
    name   = data.get("name", "Farmer")

    if otp_store.get(mobile) != otp:
        return jsonify({"error": "Invalid OTP"}), 401

    # ✅ find user via Beanie
    user = await User.find_one(User.mobile == mobile)

    # ✅ create user if not exists
    if not user:
        user = User(mobile=mobile, name=name)
        await user.insert()
        
    user_id = str(user.id)

    otp_store.pop(mobile, None)

    token = create_access_token(identity=user_id)

    return jsonify({
        "token": token,
        "user_id": user_id,
        "name": name
    }), 200