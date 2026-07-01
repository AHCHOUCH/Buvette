"""Dashboard metrics and recent activity."""
from datetime import date, datetime, time
from decimal import Decimal
from sqlalchemy import func
from app.models import Client, LedgerEntry
from app.repositories.core import BreakfastRepository, LedgerRepository, LunchRepository
from app.utils.constants import LEDGER_CREDIT, LEDGER_DEBIT
from app.utils.formatting import normalize_money

class DashboardService:
    def __init__(self, session): self.session=session
    def metrics(self):
        start=datetime.combine(date.today(), time.min)
        breakfast=BreakfastRepository(self.session).todays_count(); lunch=LunchRepository(self.session).todays_count()
        revenue=self.session.query(func.coalesce(func.sum(LedgerEntry.amount), 0)).filter(LedgerEntry.entry_type==LEDGER_CREDIT, LedgerEntry.timestamp>=start).scalar()
        outstanding=Decimal('0.00'); over_limit=0
        for client in self.session.query(Client).filter_by(is_active=True).all():
            bal=LedgerRepository(self.session).current_balance(client.id); outstanding += bal
            if client.debt_limit and client.debt_limit > 0 and bal > client.debt_limit: over_limit += 1
        ledger=LedgerService(self.session) if False else LedgerRepository(self.session)
        return {"breakfast_orders": breakfast, "lunch_orders": lunch, "todays_revenue": normalize_money(revenue or 0), "outstanding_debt": normalize_money(outstanding), "clients_over_limit": over_limit, "recent_payments": ledger.recent(LEDGER_CREDIT), "recent_charges": ledger.recent(LEDGER_DEBIT)}
