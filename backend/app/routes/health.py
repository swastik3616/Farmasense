import time
from flask import Blueprint, jsonify, current_app
from redis import Redis

health_bp = Blueprint("health", __name__)

START_TIME = time.time()

@health_bp.route("/", methods=["GET"])
async def health_check():
    status = {
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "dependencies": {}
    }

    # 1. Check MongoDB via Async Motor
    db = getattr(current_app, "db", None)
    if db is not None:
        try:
            await db.command("ping")
            status["dependencies"]["mongodb"] = "ok"
        except Exception:
            status["dependencies"]["mongodb"] = "failed"
            status["status"] = "degraded"
    else:
        status["dependencies"]["mongodb"] = "not_initialized"
        status["status"] = "degraded"

    # 2. Check Redis (used by Celery and directly)
    try:
        r = Redis(host='localhost', port=6379, db=0, socket_connect_timeout=1)
        if r.ping():
            status["dependencies"]["redis"] = "ok"
        else:
            status["dependencies"]["redis"] = "failed"
            status["status"] = "degraded"
    except Exception:
        status["dependencies"]["redis"] = "failed"
        status["status"] = "degraded"

    status_code = 200 if status["status"] == "healthy" else 503
    return jsonify(status), status_code
