from flask import Flask
from flask_jwt_extended import JWTManager
from database import db
import database.models  # noqa: F401 — registers all models with SQLAlchemy
from utils.error_handlers import register_error_handlers


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Extensions
    db.init_app(app)
    JWTManager(app)

    # Error handlers
    register_error_handlers(app)

    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register blueprints here
    # from routes.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)