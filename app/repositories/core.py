"""Repository helpers used by feature services."""

from __future__ import annotations

from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload

from app.models import (
    BreakfastOrder, BreakfastProduct, Client, LedgerEntry, LunchMenu, LunchOrder,
    ManualCharge, Payment, Setting,
)
from app.utils.constants import LEDGER_CREDIT, LEDGER_DEBIT


class ClientRepository:
    def __init__(self, session): self.session = session
    def list(self, q: str = "", include_archived: bool = False):
        query = self.session.query(Client)
        if q:
            like = f"%{q.strip()}%"
            query = query.filter(or_(Client.name.ilike(like), Client.account_code.ilike(like)))
        if not include_archived:
            query = query.filter(Client.is_active.is_(True))
        return query.order_by(Client.name).all()
    def get(self, client_id: int): return self.session.get(Client, client_id)
    def find_duplicate_identifier(self, account_code: str, exclude_id: int | None = None):
        if not account_code: return None
        query = self.session.query(Client).filter(Client.account_code == account_code, Client.is_active.is_(True))
        if exclude_id: query = query.filter(Client.id != exclude_id)
        return query.first()
    def save(self, client: Client): self.session.add(client); return client


class LedgerRepository:
    def __init__(self, session): self.session = session
    def current_balance(self, client_id: int) -> Decimal:
        debit = self.session.query(func.coalesce(func.sum(LedgerEntry.amount), 0)).filter_by(client_id=client_id, entry_type=LEDGER_DEBIT).scalar()
        credit = self.session.query(func.coalesce(func.sum(LedgerEntry.amount), 0)).filter_by(client_id=client_id, entry_type=LEDGER_CREDIT).scalar()
        return Decimal(debit or 0) - Decimal(credit or 0)
    def add(self, entry: LedgerEntry): self.session.add(entry); return entry
    def list(self, client_id=None, start_date=None, end_date=None, reference_type=None):
        query = self.session.query(LedgerEntry).options(joinedload(LedgerEntry.client))
        if client_id: query = query.filter(LedgerEntry.client_id == client_id)
        if start_date: query = query.filter(LedgerEntry.timestamp >= datetime.combine(start_date, time.min))
        if end_date: query = query.filter(LedgerEntry.timestamp <= datetime.combine(end_date, time.max))
        if reference_type: query = query.filter(LedgerEntry.reference_type == reference_type)
        return query.order_by(LedgerEntry.timestamp.desc(), LedgerEntry.id.desc()).all()
    def recent(self, entry_type: str, limit: int = 5):
        return self.session.query(LedgerEntry).options(joinedload(LedgerEntry.client)).filter_by(entry_type=entry_type).order_by(LedgerEntry.timestamp.desc()).limit(limit).all()


class BreakfastRepository:
    def __init__(self, session): self.session = session
    def products(self, active_only=True):
        q = self.session.query(BreakfastProduct)
        if active_only: q = q.filter_by(is_active=True)
        return q.order_by(BreakfastProduct.name).all()
    def product(self, product_id): return self.session.get(BreakfastProduct, product_id)
    def product_by_name(self, name): return self.session.query(BreakfastProduct).filter(func.lower(BreakfastProduct.name)==name.lower()).first()
    def save_product(self, product): self.session.add(product); return product
    def save_order(self, order): self.session.add(order); return order
    def todays_count(self): return self.session.query(BreakfastOrder).filter(BreakfastOrder.created_at >= datetime.combine(date.today(), time.min)).count()


class LunchRepository:
    def __init__(self, session): self.session = session
    def menus(self): return self.session.query(LunchMenu).order_by(LunchMenu.weekday).all()
    def menu_for_weekday(self, weekday): return self.session.query(LunchMenu).filter_by(weekday=weekday).first()
    def save_menu(self, menu): self.session.add(menu); return menu
    def save_order(self, order): self.session.add(order); return order
    def todays_count(self): return self.session.query(LunchOrder).filter_by(service_date=date.today()).count()


class ChargeRepository:
    def __init__(self, session): self.session = session
    def save(self, charge): self.session.add(charge); return charge


class PaymentRepository:
    def __init__(self, session): self.session = session
    def save(self, payment): self.session.add(payment); return payment
    def history(self): return self.session.query(Payment).options(joinedload(Payment.client)).order_by(Payment.created_at.desc()).limit(50).all()


class SettingsRepository:
    def __init__(self, session): self.session = session
    def get(self, key, default=""):
        setting = self.session.get(Setting, key)
        return setting.value if setting else default
    def set(self, key, value):
        setting = self.session.get(Setting, key) or Setting(key=key, value=str(value))
        setting.value = str(value)
        self.session.add(setting)
        return setting
