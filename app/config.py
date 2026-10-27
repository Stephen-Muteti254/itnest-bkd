import os
from datetime import timedelta
from dotenv import load_dotenv
import json

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    SQLALCHEMY_DATABASE_URI = (
        f"{os.getenv('DATABASE_URL')}"
        f"?sslmode=verify-full"
        f"&sslrootcert={os.getenv('DB_SSLROOTCERT')}"
    )

    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8080"
    )

    RATELIMIT_HEADERS_ENABLED = True

    FREE_ORDER_LIMIT = int(os.getenv("FREE_ORDER_LIMIT", 2))

    ACCESS_EXPIRES = int(os.getenv("ACCESS_EXPIRES", 86400))
    REFRESH_EXPIRES = int(os.getenv("REFRESH_EXPIRES", 86400))
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    UPLOAD_ROOT = os.getenv("UPLOAD_ROOT", "/var/data/uploads")

    UPLOAD_FOLDER = os.path.join(UPLOAD_ROOT, "applications")
    ORDERS_FOLDER = os.path.join(UPLOAD_ROOT, "orders")
    SUBMISSIONS_FOLDER = os.path.join(UPLOAD_ROOT, "submissions")
    SUPPORT_UPLOADS_FOLDER = os.path.join(UPLOAD_ROOT, "support_chats")
    PROFILES_FOLDER = os.path.join(UPLOAD_ROOT, "profiles")
    CAREERS_UPLOAD_FOLDER = os.path.join(UPLOAD_ROOT, "careers")
    INSIGHTPAY_SURVEY_UPLOADS_FOLDER = os.path.join(UPLOAD_ROOT, "insightpay_surveys")

    EMAIL_VERIFY_EXPIRES = int(os.getenv("EMAIL_VERIFY_EXPIRES", 3600))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
