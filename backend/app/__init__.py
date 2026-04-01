from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    # Initialize LangChain Global Caching (if set up)
    from app.agents.cache import init_semantic_cache
    init_semantic_cache()
    
    @app.before_request
    async def initialize_database():
        if not getattr(app, "db_initialized", False):
            from app.database import init_db
            await init_db(app)
            app.db_initialized = True

    from app.routes.auth     import auth_bp
    from app.routes.farm     import farm_bp
    from app.routes.advisory import advisory_bp
    from app.routes.market   import market_bp
    from app.routes.alerts   import alerts_bp
    from app.routes.admin    import admin_bp
    from app.routes.health   import health_bp

    app.register_blueprint(auth_bp,     url_prefix="/api/auth")
    app.register_blueprint(farm_bp,     url_prefix="/api/farm")
    app.register_blueprint(advisory_bp, url_prefix="/api/advisory")
    app.register_blueprint(market_bp,   url_prefix="/api/market")
    app.register_blueprint(alerts_bp,   url_prefix="/api/alerts")
    app.register_blueprint(admin_bp,    url_prefix="/api/admin")
    app.register_blueprint(health_bp,   url_prefix="/api/health")

    return app