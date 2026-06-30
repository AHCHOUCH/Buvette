"""Centralized database models for Buvette Manager."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from app import db
from app.utils.constants import LEDGER_CREDIT, LEDGER_DEBIT, ROLE_CASHIER


class User(db.Model):
    """Authenticated application user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(30), nullable=False, default=ROLE_CASHIER)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    ledger_entries = db.relationship("LedgerEntry", back_populates="created_by_user")

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
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    ledger_entries = db.relationship(
        "LedgerEntry",
        back_populates="client",
        order_by="LedgerEntry.timestamp"
    )

    def __repr__(self) -> str:
        return f"<Client {self.name}>"


class LedgerEntry(db.Model):
    """Normalized financial ledger row for future posting workflows."""

    __tablename__ = "ledger_entries"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False, index=True)
    entry_type = db.Column(db.String(10), nullable=False, index=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    running_balance = db.Column(db.Numeric(12, 2), nullable=False)
    reference_type = db.Column(db.String(50), nullable=True, index=True)
    reference_id = db.Column(db.Integer, nullable=True, index=True)
    description = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    client = db.relationship("Client", back_populates="ledger_entries")
    created_by_user = db.relationship("User", back_populates="ledger_entries")

    __table_args__ = (
        db.CheckConstraint("entry_type in ('debit', 'credit')", name="ck_ledger_entries_entry_type"),
        db.CheckConstraint("amount >= 0", name="ck_ledger_entries_amount_non_negative"),
    )

    def signed_amount(self) -> Decimal:
        """Return debit as positive and credit as negative for balance math."""

        if self.entry_type == LEDGER_CREDIT:
            return -self.amount
        if self.entry_type == LEDGER_DEBIT:
            return self.amount
        raise ValueError(f"Unsupported ledger entry type: {self.entry_type}")

    def __repr__(self) -> str:
        return f"<LedgerEntry client={self.client_id} type={self.entry_type} amount={self.amount}>"


__all__ = ["Client", "LedgerEntry", "User"]
