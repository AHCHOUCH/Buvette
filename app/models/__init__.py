"""Centralized database models for Buvette Manager."""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from app import db
from app.utils.constants import LEDGER_CREDIT, LEDGER_DEBIT, ROLE_CASHIER


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(db.Model):
    """Authenticated application user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False, default="")
    full_name = db.Column(db.String(120), nullable=False, default="")
    display_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(30), nullable=False, default=ROLE_CASHIER)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    active = db.synonym("is_active")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)
    last_login_at = db.Column(db.DateTime(timezone=True), nullable=True)

    ledger_entries = db.relationship("LedgerEntry", back_populates="created_by_user")

    @property
    def is_authenticated(self): return True
    @property
    def is_anonymous(self): return False
    def get_id(self) -> str: return str(self.id)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Client(db.Model):
    """Client account used by financial workflows."""

    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False, index=True)
    account_code = db.Column(db.String(50), unique=True, nullable=True, index=True)
    debt_limit = db.Column(db.Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    ledger_entries = db.relationship("LedgerEntry", back_populates="client", order_by="LedgerEntry.timestamp", cascade="all, delete-orphan")
    breakfast_orders = db.relationship("BreakfastOrder", back_populates="client")
    lunch_orders = db.relationship("LunchOrder", back_populates="client")
    payments = db.relationship("Payment", back_populates="client")

    @property
    def employee_number(self) -> str | None:
        return self.account_code

    @employee_number.setter
    def employee_number(self, value: str | None) -> None:
        self.account_code = value

    def __repr__(self) -> str:
        return f"<Client {self.name}>"


class LedgerEntry(db.Model):
    """Normalized financial ledger row for all posted transactions."""

    __tablename__ = "ledger_entries"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False, index=True)
    entry_type = db.Column(db.String(10), nullable=False, index=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    running_balance = db.Column(db.Numeric(12, 2), nullable=False)
    reference_type = db.Column(db.String(50), nullable=True, index=True)
    reference_id = db.Column(db.Integer, nullable=True, index=True)
    description = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, index=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    client = db.relationship("Client", back_populates="ledger_entries")
    created_by_user = db.relationship("User", back_populates="ledger_entries")

    __table_args__ = (
        db.CheckConstraint("entry_type in ('debit', 'credit')", name="ck_ledger_entries_entry_type"),
        db.CheckConstraint("amount >= 0", name="ck_ledger_entries_amount_non_negative"),
        db.Index("ix_ledger_client_timestamp", "client_id", "timestamp"),
    )

    def signed_amount(self) -> Decimal:
        if self.entry_type == LEDGER_CREDIT:
            return -self.amount
        if self.entry_type == LEDGER_DEBIT:
            return self.amount
        raise ValueError(f"Unsupported ledger entry type: {self.entry_type}")


class BreakfastProduct(db.Model):
    __tablename__ = "breakfast_products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True, index=True)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    __table_args__ = (db.CheckConstraint("price >= 0", name="ck_breakfast_products_price_non_negative"),)


class BreakfastOrder(db.Model):
    __tablename__ = "breakfast_orders"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False, index=True)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, index=True)

    client = db.relationship("Client", back_populates="breakfast_orders")
    items = db.relationship("BreakfastOrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (db.CheckConstraint("total_amount >= 0", name="ck_breakfast_orders_total_non_negative"),)


class BreakfastOrderItem(db.Model):
    __tablename__ = "breakfast_order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("breakfast_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("breakfast_products.id"), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    line_total = db.Column(db.Numeric(12, 2), nullable=False)

    order = db.relationship("BreakfastOrder", back_populates="items")
    product = db.relationship("BreakfastProduct")

    __table_args__ = (
        db.CheckConstraint("unit_price >= 0", name="ck_breakfast_items_price_non_negative"),
        db.CheckConstraint("quantity > 0", name="ck_breakfast_items_quantity_positive"),
        db.CheckConstraint("line_total >= 0", name="ck_breakfast_items_total_non_negative"),
    )


class WeeklyMenu(db.Model):
    __tablename__ = "weekly_menus"
    id = db.Column(db.Integer, primary_key=True)
    week_start_date = db.Column(db.Date, nullable=False, unique=True, index=True)
    label = db.Column(db.String(160), nullable=False, default="")
    active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)
    days = db.relationship("DailyMenu", back_populates="weekly_menu", cascade="all, delete-orphan")


class DailyMenu(db.Model):
    __tablename__ = "daily_menus"
    id = db.Column(db.Integer, primary_key=True)
    weekly_menu_id = db.Column(db.Integer, db.ForeignKey("weekly_menus.id"), nullable=False, index=True)
    service_date = db.Column(db.Date, nullable=False, index=True)
    weekday = db.Column(db.Integer, nullable=False, index=True)
    active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    weekly_menu = db.relationship("WeeklyMenu", back_populates="days")
    plates = db.relationship("FoodPlate", back_populates="daily_menu", cascade="all, delete-orphan")
    __table_args__ = (db.UniqueConstraint("weekly_menu_id", "service_date", name="uq_daily_menu_week_date"),)


class FoodPlate(db.Model):
    __tablename__ = "food_plates"
    id = db.Column(db.Integer, primary_key=True)
    daily_menu_id = db.Column(db.Integer, db.ForeignKey("daily_menus.id"), nullable=False, index=True)
    name = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    daily_menu = db.relationship("DailyMenu", back_populates="plates")
    variants = db.relationship("FoodPlateVariant", back_populates="food_plate", cascade="all, delete-orphan")


class FoodPlateVariant(db.Model):
    __tablename__ = "food_plate_variants"
    id = db.Column(db.Integer, primary_key=True)
    food_plate_id = db.Column(db.Integer, db.ForeignKey("food_plates.id"), nullable=False, index=True)
    size_key = db.Column(db.String(30), nullable=False)
    label = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    food_plate = db.relationship("FoodPlate", back_populates="variants")
    __table_args__ = (db.CheckConstraint("price >= 0", name="ck_food_plate_variants_price_non_negative"),)


class LunchMenu(db.Model):
    __tablename__ = "lunch_menus"

    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.Integer, nullable=False, unique=True, index=True)
    name = db.Column(db.String(160), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        db.CheckConstraint("weekday between 0 and 6", name="ck_lunch_menus_weekday"),
        db.CheckConstraint("price >= 0", name="ck_lunch_menus_price_non_negative"),
    )


class LunchOrder(db.Model):
    __tablename__ = "lunch_orders"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False, index=True)
    menu_id = db.Column(db.Integer, db.ForeignKey("lunch_menus.id"), nullable=True)
    food_plate_id = db.Column(db.Integer, db.ForeignKey("food_plates.id"), nullable=True, index=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("food_plate_variants.id"), nullable=True, index=True)
    service_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    menu_name = db.Column(db.String(160), nullable=False, default="")
    plate_name_snapshot = db.Column(db.String(160), nullable=False, default="")
    variant_label_snapshot = db.Column(db.String(80), nullable=False, default="")
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, index=True)

    client = db.relationship("Client", back_populates="lunch_orders")
    menu = db.relationship("LunchMenu")
    food_plate = db.relationship("FoodPlate")
    variant = db.relationship("FoodPlateVariant")

    __table_args__ = (db.CheckConstraint("amount >= 0", name="ck_lunch_orders_amount_non_negative"),)


class Supplier(db.Model):
    __tablename__ = "suppliers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(80), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)
    charges = db.relationship("ManualCharge", back_populates="supplier")


class ManualCharge(db.Model):
    __tablename__ = "manual_charges"

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=True, index=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    category = db.Column(db.String(80), nullable=False, index=True)
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, index=True)

    supplier = db.relationship("Supplier", back_populates="charges")

    __table_args__ = (db.CheckConstraint("amount >= 0", name="ck_manual_charges_amount_non_negative"),)


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False, index=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    note = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, index=True)

    client = db.relationship("Client", back_populates="payments")

    __table_args__ = (db.CheckConstraint("amount >= 0", name="ck_payments_amount_non_negative"),)


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    username_snapshot = db.Column(db.String(80), nullable=True, index=True)
    action = db.Column(db.String(120), nullable=False, index=True)
    entity_type = db.Column(db.String(80), nullable=True, index=True)
    entity_id = db.Column(db.Integer, nullable=True, index=True)
    description = db.Column(db.Text, nullable=False, default="")
    ip_address = db.Column(db.String(80), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    severity = db.Column(db.String(20), nullable=False, default="INFO", index=True)
    metadata_json = db.Column(db.Text, nullable=True)


class Setting(db.Model):
    __tablename__ = "settings"

    key = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)


__all__ = [
    "BreakfastOrder", "BreakfastOrderItem", "BreakfastProduct", "Client", "LedgerEntry",
    "LunchMenu", "WeeklyMenu", "DailyMenu", "FoodPlate", "FoodPlateVariant", "LunchOrder", "ManualCharge", "Payment", "Setting", "Supplier", "AuditLog", "User",
]
