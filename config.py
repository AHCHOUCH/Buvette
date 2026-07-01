"""Configuration objects for Buvette Manager."""

import os


class Config:
    """Base application configuration."""

    APP_NAME = "Buvette Manager"
    ENVIRONMENT = os.environ.get("FLASK_ENV", os.environ.get("APP_ENV", "development"))
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///buvette-manager.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
