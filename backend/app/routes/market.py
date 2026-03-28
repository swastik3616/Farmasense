from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests, os

market_bp = Blueprint("market", __name__)

@market_bp.route("/prices/<district>", methods=["GET"])
@jwt_required()
def get_prices(district):
    crops   = request.args.get("crops", "Rice,Wheat,Tomato,Onion,Maize").split(",")
    api_key = os.getenv("MANDI_API_KEY")
    prices  = {}

    for crop in crops:
        url = (
            f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
            f"?api-key={api_key}&format=json"
            f"&filters[District]={district}&filters[Commodity]={crop}&limit=5"
        )
        try:
            res     = requests.get(url, timeout=5)
            data    = res.json()
            records = data.get("records", [])
            if records:
                latest       = records[0]
                prices[crop] = {
                    "modal_price": latest.get("Modal_x0020_Price", 0),
                    "min_price"  : latest.get("Min_x0020_Price", 0),
                    "max_price"  : latest.get("Max_x0020_Price", 0),
                    "market"     : latest.get("Market", district),
                }
        except Exception as e:
            prices[crop] = {"error": str(e)}

    return jsonify(prices), 200


@market_bp.route("/predict/<crop>/<district>", methods=["GET"])
@jwt_required()
def predict_price(crop, district):
    # Placeholder — ML model integration in Week 3
    return jsonify({
        "crop"            : crop,
        "district"        : district,
        "current_price"   : 1200,
        "predicted_30_day": 1450,
        "predicted_90_day": 1800,
        "trend"           : "rising",
        "confidence"      : 0.78,
    }), 200