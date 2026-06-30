"""Configuration objects for Buvette Manager."""

import os


class Config:
    """Base application configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///buvette-manager.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
