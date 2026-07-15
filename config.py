import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "gastronomic_erp.db"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{DB_PATH.as_posix()}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask session-based authentication
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set True in production (HTTPS)
    SESSION_COOKIE_SAMESITE = "Lax"