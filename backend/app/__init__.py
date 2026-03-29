from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

from config import Config

db           = SQLAlchemy()
jwt          = JWTManager()
mongo_client = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    global mongo_client
    mongo_client = MongoClient(app.config["MONGO_URI"])

    from app.routes.auth     import auth_bp
    from app.routes.farm     import farm_bp
    from app.routes.advisory import advisory_bp
    from app.routes.market   import market_bp
    from app.routes.alerts   import alerts_bp
    from app.routes.admin    import admin_bp

    app.register_blueprint(auth_bp,     url_prefix="/api/auth")
    app.register_blueprint(farm_bp,     url_prefix="/api/farm")
    app.register_blueprint(advisory_bp, url_prefix="/api/advisory")
    app.register_blueprint(market_bp,   url_prefix="/api/market")
    app.register_blueprint(alerts_bp,   url_prefix="/api/alerts")
    app.register_blueprint(admin_bp,    url_prefix="/api/admin")

    with app.app_context():
        db.create_all()

    return app