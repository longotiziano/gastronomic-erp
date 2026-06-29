import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///gastronomic_erp.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT stored in HTTPOnly cookies
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SECURE = False          # Set True in production (HTTPS)
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 8  # 8 hours