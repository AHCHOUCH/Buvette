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
    _register_template_helpers(app)
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
    login_manager.login_message = "Veuillez vous connecter."
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
    from app.users.routes import users_bp
    from app.logs.routes import logs_bp

    blueprints = (auth_bp, dashboard_bp, clients_bp, breakfast_bp, lunch_bp, charges_bp, payments_bp, ledger_bp, settings_bp, users_bp, logs_bp)
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
    from app import db
    from app.audit import log_audit

    def handle_error(error, status_code):
        db.session.rollback()
        if status_code == 500:
            try:
                log_audit('error.500', 'Error', None, str(error), severity='ERROR')
                db.session.commit()
            except Exception:
                db.session.rollback()
        return render_template("errors/error.html", status_code=status_code, error=error), status_code

    for code in (400, 403, 404, 500):
        app.register_error_handler(
            code,
            lambda error, status_code=code: handle_error(error, status_code),
        )



def _register_template_helpers(app: Flask) -> None:
    from app.i18n import _, lang, direction, weekday_key
    from app.permissions import has_permission
    from app.settings.service import SettingsService
    @app.context_processor
    def helpers():
        groups = [
            ('nav.operations', [('nav.dashboard','dashboard.index','dashboard.view'),('nav.breakfast','breakfast.index','breakfast.sell'),('nav.lunch','lunch.index','lunch.sell'),('nav.payments','payments.index','payments.create')]),
            ('nav.management', [('nav.clients','clients.index','clients.manage'),('nav.products','breakfast.products','breakfast.manage'),('nav.menus','lunch.menus','lunch.manage'),('nav.suppliers','charges.suppliers','suppliers.manage'),('nav.expenses','charges.index','expenses.manage')]),
            ('nav.finance', [('nav.ledger','ledger.index','ledger.view')]),
            ('nav.admin', [('nav.users','users.index','users.manage'),('nav.settings','settings.index','settings.manage'),('nav.logs','logs.index','logs.view')]),
        ]
        filtered=[]
        for label, items in groups:
            visible=[i for i in items if has_permission(i[2]) or (i[2]=='dashboard.view' and has_permission('dashboard.view_limited'))]
            if visible: filtered.append((label, visible))
        
        def variant_label(variant):
            key = getattr(variant, 'size_key', '') or getattr(variant, 'label', '')
            return _(f'variant.{key}') if key in ('small', 'big') else getattr(variant, 'label', '')
        identity = SettingsService(db.session).identity()
        return {'_': _, 'weekday_key': weekday_key, 'variant_label': variant_label, 'ui_lang': lang(), 'ui_dir': direction(), 'nav_groups': filtered, 'identity': identity}

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
        _ensure_sqlite_columns()
        _seed_data()



def _ensure_sqlite_columns() -> None:
    """Apply tiny additive SQLite compatibility upgrades for local MVP databases."""
    from sqlalchemy import inspect, text
    inspector = inspect(db.engine)
    tables = set(inspector.get_table_names())
    def cols(table): return {c['name'] for c in inspector.get_columns(table)} if table in tables else set()
    statements=[]
    user_cols=cols('users')
    for name, ddl in {"password_hash":"VARCHAR(255) DEFAULT ''","full_name":"VARCHAR(120) DEFAULT ''","updated_at":"DATETIME","last_login_at":"DATETIME"}.items():
        if 'users' in tables and name not in user_cols: statements.append(f'ALTER TABLE users ADD COLUMN {name} {ddl}')
    charge_cols=cols('manual_charges')
    if 'manual_charges' in tables and 'supplier_id' not in charge_cols: statements.append('ALTER TABLE manual_charges ADD COLUMN supplier_id INTEGER')
    if 'manual_charges' in tables and 'created_by_user_id' not in charge_cols: statements.append('ALTER TABLE manual_charges ADD COLUMN created_by_user_id INTEGER')
    product_cols=cols('breakfast_products')
    if 'breakfast_products' in tables and 'product_type' not in product_cols: statements.append("ALTER TABLE breakfast_products ADD COLUMN product_type VARCHAR(30) NOT NULL DEFAULT 'breakfast'")
    if 'breakfast_products' in tables and 'archived_at' not in product_cols: statements.append('ALTER TABLE breakfast_products ADD COLUMN archived_at DATETIME')

    # Weekly menu compatibility columns for local SQLite databases. Production should apply migrations/0004_weekly_menu_i18n_permissions.sql.
    lunch_cols=cols('lunch_orders')
    if 'lunch_order_items' not in tables:
        statements.append("CREATE TABLE lunch_order_items (id INTEGER PRIMARY KEY, lunch_order_id INTEGER NOT NULL, product_id INTEGER, product_name_snapshot VARCHAR(120) NOT NULL, quantity INTEGER NOT NULL, unit_price_snapshot NUMERIC(12,2) NOT NULL, total NUMERIC(12,2) NOT NULL)")
    if 'lunch_orders' in tables:
        for name, ddl in {'food_plate_id':'INTEGER','variant_id':'INTEGER','plate_name_snapshot':"VARCHAR(160) DEFAULT ''",'variant_label_snapshot':"VARCHAR(80) DEFAULT ''",'created_by_user_id':'INTEGER'}.items():
            if name not in lunch_cols: statements.append(f'ALTER TABLE lunch_orders ADD COLUMN {name} {ddl}')
    for statement in statements:
        db.session.execute(text(statement))
    if statements: db.session.commit()
    if 'lunch_order_items' not in tables:
        statements.append("CREATE TABLE lunch_order_items (id INTEGER PRIMARY KEY, lunch_order_id INTEGER NOT NULL, product_id INTEGER, product_name_snapshot VARCHAR(120) NOT NULL, quantity INTEGER NOT NULL, unit_price_snapshot NUMERIC(12,2) NOT NULL, total NUMERIC(12,2) NOT NULL)")
    if 'lunch_orders' in tables:
        menu_col = next((c for c in inspector.get_columns('lunch_orders') if c['name'] == 'menu_id'), None)
        if menu_col and not menu_col.get('nullable', True):
            _rebuild_lunch_orders_nullable_menu_id()


def _rebuild_lunch_orders_nullable_menu_id() -> None:
    """Rebuild local SQLite lunch_orders when legacy menu_id is NOT NULL."""
    from sqlalchemy import text
    db.session.execute(text('PRAGMA foreign_keys=off'))
    db.session.execute(text('DROP TABLE IF EXISTS lunch_orders_new'))
    db.session.execute(text("""
        CREATE TABLE lunch_orders_new (
          id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL, menu_id INTEGER NULL,
          food_plate_id INTEGER NULL, variant_id INTEGER NULL, service_date DATE NOT NULL,
          menu_name VARCHAR(160) NOT NULL DEFAULT '', plate_name_snapshot VARCHAR(160) NOT NULL DEFAULT '',
          variant_label_snapshot VARCHAR(80) NOT NULL DEFAULT '', created_by_user_id INTEGER NULL,
          amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0), created_at DATETIME NOT NULL
        )
    """))
    from sqlalchemy import inspect
    existing = {c['name'] for c in inspect(db.engine).get_columns('lunch_orders')}
    cols = ['id','client_id','menu_id','food_plate_id','variant_id','service_date','menu_name','plate_name_snapshot','variant_label_snapshot','created_by_user_id','amount','created_at']
    select_cols = [col if col in existing else "''" if col in ('menu_name','plate_name_snapshot','variant_label_snapshot') else 'NULL' for col in cols]
    db.session.execute(text(f"INSERT INTO lunch_orders_new ({','.join(cols)}) SELECT {','.join(select_cols)} FROM lunch_orders"))
    db.session.execute(text('DROP TABLE lunch_orders'))
    db.session.execute(text('ALTER TABLE lunch_orders_new RENAME TO lunch_orders'))
    for stmt in ('CREATE INDEX IF NOT EXISTS ix_lunch_orders_client_id ON lunch_orders(client_id)', 'CREATE INDEX IF NOT EXISTS ix_lunch_orders_service_date ON lunch_orders(service_date)', 'CREATE INDEX IF NOT EXISTS ix_lunch_orders_food_plate_id ON lunch_orders(food_plate_id)', 'CREATE INDEX IF NOT EXISTS ix_lunch_orders_variant_id ON lunch_orders(variant_id)'):
        db.session.execute(text(stmt))
    db.session.execute(text('PRAGMA foreign_keys=on'))
    db.session.commit()

def _seed_data() -> None:
    """Seed default products, menus, settings, and a sample client for first use."""

    from app.models import BreakfastProduct, Client, LunchMenu, Setting, User, Supplier
    from werkzeug.security import generate_password_hash
    from app.utils.constants import ROLE_ADMIN, ROLE_CASHIER

    if not User.query.first():
        db.session.add(User(username="administrator", full_name="Administrator", display_name="Administrator", role=ROLE_ADMIN, password_hash=generate_password_hash("administrator")))
        db.session.add(User(username="cashier", full_name="Cashier", display_name="Cashier", role=ROLE_CASHIER, password_hash=generate_password_hash("cashier")))
    if not Client.query.first():
        db.session.add(Client(name="Walk-in Staff", account_code="EMP-0001", debt_limit=50, notes="Default staff account"))
    if not BreakfastProduct.query.first():
        for name, price in (("Café", 5.00), ("Thé", 4.00), ("Croissant", 8.00), ("Sandwich", 15.00)):
            db.session.add(BreakfastProduct(name=name, price=price, is_active=True))
    if not Supplier.query.first():
        for name in ("Carrefour", "Marjane", "Local bakery", "Vegetable supplier", "Cleaning supplier", "Other"):
            db.session.add(Supplier(name=name, active=True))
    if not LunchMenu.query.first():
        menus = ((0, "Monday hot meal", 6.00), (1, "Tuesday pasta", 6.00), (2, "Wednesday grill", 6.50), (3, "Thursday special", 6.00), (4, "Friday fish", 7.00))
        for weekday, name, price in menus:
            db.session.add(LunchMenu(weekday=weekday, name=name, price=price, is_active=True))
    for key, value in {"organization_name": "Buvette Manager", "debt_warning_default": "50.00", "currency": "DH", "primary_color": "#2f6f73", "secondary_color": "#eef2f4", "accent_color": "#0d6efd", "header_background_color": "#2f6f73", "sidebar_background_color": "#eaf3f3", "button_color": "#2f6f73", "login_background_color": "#f6f7f9"}.items():
        if not db.session.get(Setting, key):
            db.session.add(Setting(key=key, value=value))
    db.session.commit()
