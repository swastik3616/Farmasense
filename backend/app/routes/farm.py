from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.models import Farm

farm_bp = Blueprint("farm", __name__)

@farm_bp.route("/create", methods=["POST"])
@jwt_required()
def create_farm():
    user_id = int(get_jwt_identity())
    data    = request.get_json()

    farm = Farm(
        user_id         = user_id,
        name            = data.get("name", "My Farm"),
        latitude        = data.get("latitude"),
        longitude       = data.get("longitude"),
        land_size_acres = data.get("land_size_acres"),
        water_source    = data.get("water_source"),
        district        = data.get("district"),
        state           = data.get("state"),
        soil_health_card_no = data.get("soil_health_card_number"),
    )
    db.session.add(farm)
    db.session.commit()
    return jsonify({"message": "Farm created", "farm_id": farm.id}), 201


@farm_bp.route("/<int:farm_id>", methods=["GET"])
@jwt_required()
def get_farm(farm_id):
    farm = Farm.query.get_or_404(farm_id)
    return jsonify({
        "id"             : farm.id,
        "name"           : farm.name,
        "latitude"       : farm.latitude,
        "longitude"      : farm.longitude,
        "land_size_acres": farm.land_size_acres,
        "water_source"   : farm.water_source,
        "soil_type"      : farm.soil_type,
        "district"       : farm.district,
        "state"          : farm.state,
    }), 200


@farm_bp.route("/<int:farm_id>", methods=["PUT"])
@jwt_required()
def update_farm(farm_id):
    farm = Farm.query.get_or_404(farm_id)
    data = request.get_json()
    farm.name            = data.get("name", farm.name)
    farm.land_size_acres = data.get("land_size_acres", farm.land_size_acres)
    farm.water_source    = data.get("water_source", farm.water_source)
    db.session.commit()
    return jsonify({"message": "Farm updated"}), 200