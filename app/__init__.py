"""Buvette Manager application package."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


def create_app(config_class: type[Config] = Config) -> Flask:
    """Create and configure the Flask application.

    Blueprints remain unregistered until each feature workflow is approved, but
    extensions are initialized now so domain models and services share one
    consistent database handle.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    return app
