import os

from flask import Flask
from database import db
import database.models  # noqa: F401 — registers all models with SQLAlchemy
from seed_data import load_initial_data
from utils.error_handlers import register_error_handlers

def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # CSRF protection
    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect(app)

    # Extensions
    db.init_app(app)

    # Error handlers
    register_error_handlers(app)

    # Create all tables if they don't exist; in development, rebuild from scratch when requested
    with app.app_context():
        db_path = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if db_path.startswith("sqlite"):
            db_file = db_path.replace("sqlite:///", "", 1)
            if db_file and db_file != ":memory:":
                os.makedirs(os.path.dirname(db_file), exist_ok=True)
        if os.getenv("RESET_DB") == "1" or app.debug:
            db.drop_all()
        db.create_all()
        try:
            load_initial_data()
        except Exception as e:
            print(f"Error loading initial data: {e}")

    from routers.main import main_bp
    app.register_blueprint(main_bp)
    from routers.auth import auth_bp
    app.register_blueprint(auth_bp)
    from routers.admin.users import users_bp
    app.register_blueprint(users_bp)
    from routers.admin.bars import bars_bp
    app.register_blueprint(bars_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)