from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db, mongo_client
from app.models.models import Farm, Advisory
from datetime import datetime

advisory_bp = Blueprint("advisory", __name__)

@advisory_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate():
    data    = request.get_json()
    farm_id = data.get("farm_id")
    farm    = Farm.query.get_or_404(farm_id)

    farm_dict = {
        "id"              : farm.id,
        "latitude"        : farm.latitude,
        "longitude"       : farm.longitude,
        "district"        : farm.district,
        "state"           : farm.state,
        "soil_type"       : farm.soil_type,
        "soil_card_number": farm.soil_health_card_no,
        "land_size_acres" : farm.land_size_acres,
        "water_source"    : farm.water_source,
    }

    # Import here to avoid circular imports
    from app.agents.orchestrator import generate_advisory
    result = generate_advisory(farm_dict)

    # Save to MongoDB
    mongo_db     = mongo_client["farmsense"]
    mongo_report = mongo_db["advisory_reports"].insert_one({
        "farm_id"   : farm_id,
        "result"    : result,
        "created_at": datetime.utcnow(),
    })

    # Save summary to SQL Server
    advisory = Advisory(
        farm_id         = farm_id,
        season          = result.get("season"),
        mongo_report_id = str(mongo_report.inserted_id),
    )
    db.session.add(advisory)
    db.session.commit()

    return jsonify({
        "advisory_id"   : advisory.id,
        "season"        : result["season"],
        "final_advisory": result["final_advisory"],
    }), 200


@advisory_bp.route("/history/<int:farm_id>", methods=["GET"])
@jwt_required()
def history(farm_id):
    advisories = Advisory.query.filter_by(farm_id=farm_id)\
                               .order_by(Advisory.created_at.desc()).all()
    return jsonify([{
        "id"        : a.id,
        "season"    : a.season,
        "created_at": str(a.created_at),
    } for a in advisories]), 200