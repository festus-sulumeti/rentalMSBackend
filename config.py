import os
from datetime import timedelta

from dotenv import load_dotenv
from sqlalchemy.engine import make_url

load_dotenv()


def database_uri():
    value = os.getenv("DATABASE_URL", "sqlite:///rentalms.db").replace("postgres://", "postgresql://", 1)
    try:
        make_url(value)
    except (TypeError, ValueError):
        return "sqlite:///rentalms.db"
    return value


class Config:
    SQLALCHEMY_DATABASE_URI = database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-development-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_HOURS", "24")))
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    CORS_ORIGINS = tuple(
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5174,http://127.0.0.1:5174",
        ).split(",")
        if origin.strip()
    )
