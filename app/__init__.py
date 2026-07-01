"""Buvette Manager application package."""

from __future__ import annotations

import logging
from pathlib import Path

from flask import Flask, jsonify, redirect, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_class: type[Config] = Config) -> Flask:
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app.config.from_object(config_class)

    _configure_logging(app)
    _init_extensions(app)
    _register_blueprints(app)
    _register_default_routes(app)
    _register_error_handlers(app)
    _ensure_database(app)

    return app


def _configure_logging(app: Flask) -> None:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
    app.logger.setLevel(logging.INFO)


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."
    login_manager.login_message_category = "warning"

    from app.auth.service import get_user_by_id

    @login_manager.user_loader
    def load_user(user_id: str):
        return get_user_by_id(user_id)


def _register_blueprints(app: Flask) -> None:
    from app.auth.routes import auth_bp
    from app.breakfast.routes import breakfast_bp
    from app.charges.routes import charges_bp
    from app.clients.routes import clients_bp
    from app.dashboard.routes import dashboard_bp
    from app.ledger.routes import ledger_bp
    from app.lunch.routes import lunch_bp
    from app.payments.routes import payments_bp
    from app.settings.routes import settings_bp

    blueprints = (auth_bp, dashboard_bp, clients_bp, breakfast_bp, lunch_bp, charges_bp, payments_bp, ledger_bp, settings_bp)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def _register_default_routes(app: Flask) -> None:
    @app.get("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.index"))
        return redirect(url_for("auth.login"))

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200


def _register_error_handlers(app: Flask) -> None:
    from flask import render_template

    for code in (400, 403, 404, 500):
        app.register_error_handler(
            code,
            lambda error, status_code=code: (
                render_template("errors/error.html", status_code=status_code, error=error),
                status_code,
            ),
        )


def _ensure_database(app: Flask) -> None:
    """Create the SQLite database automatically when no database file exists."""

    from app import models  # noqa: F401 - importing registers model metadata

    with app.app_context():
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if uri.startswith("sqlite:///"):
            db_path = Path(uri.removeprefix("sqlite:///"))
            if not db_path.is_absolute():
                db_path = Path(app.instance_path) / db_path
            db_path.parent.mkdir(parents=True, exist_ok=True)
        db.create_all()
        _seed_data()


def _seed_data() -> None:
    """Seed default products, menus, settings, and a sample client for first use."""

    from app.models import BreakfastProduct, Client, LunchMenu, Setting

    if not Client.query.first():
        db.session.add(Client(name="Walk-in Staff", account_code="STAFF", debt_limit=50, notes="Default staff account"))
    if not BreakfastProduct.query.first():
        for name, price in (("Coffee", 1.00), ("Tea", 0.80), ("Croissant", 1.50), ("Sandwich", 2.50)):
            db.session.add(BreakfastProduct(name=name, price=price, is_active=True))
    if not LunchMenu.query.first():
        menus = ((0, "Monday hot meal", 6.00), (1, "Tuesday pasta", 6.00), (2, "Wednesday grill", 6.50), (3, "Thursday special", 6.00), (4, "Friday fish", 7.00))
        for weekday, name, price in menus:
            db.session.add(LunchMenu(weekday=weekday, name=name, price=price, is_active=True))
    for key, value in {"organization_name": "Company Buvette", "debt_warning_default": "50.00", "currency": "€"}.items():
        if not db.session.get(Setting, key):
            db.session.add(Setting(key=key, value=value))
    db.session.commit()
