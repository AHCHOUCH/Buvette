"""Dashboard metrics and recent activity."""
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from sqlalchemy import func
from app.models import BreakfastOrder, Client, LedgerEntry, LunchOrder, ManualCharge, Payment
from app.repositories.core import LedgerRepository
from app.utils.constants import LEDGER_CREDIT, LEDGER_DEBIT, REFERENCE_BREAKFAST, REFERENCE_LUNCH
from app.utils.formatting import normalize_money

class DashboardService:
    def __init__(self, session): self.session=session
    def _sum_ledger(self, reference_type=None, entry_type=None, start=None):
        q=self.session.query(func.coalesce(func.sum(LedgerEntry.amount), 0))
        if reference_type: q=q.filter(LedgerEntry.reference_type==reference_type)
        if entry_type: q=q.filter(LedgerEntry.entry_type==entry_type)
        if start: q=q.filter(LedgerEntry.timestamp>=start)
        return normalize_money(q.scalar() or 0)
    def metrics(self):
        today_start=datetime.combine(date.today(), time.min); period_start=today_start - timedelta(days=29); days=30
        breakfast_revenue=self._sum_ledger(REFERENCE_BREAKFAST, LEDGER_DEBIT, today_start)
        lunch_revenue=self._sum_ledger(REFERENCE_LUNCH, LEDGER_DEBIT, today_start)
        payments_today=normalize_money(self.session.query(func.coalesce(func.sum(Payment.amount),0)).filter(Payment.created_at>=today_start).scalar() or 0)
        expenses_today=normalize_money(self.session.query(func.coalesce(func.sum(ManualCharge.amount),0)).filter(ManualCharge.created_at>=today_start).scalar() or 0)
        outstanding=Decimal('0.00'); over_limit=0
        ledger_repo=LedgerRepository(self.session)
        for client in self.session.query(Client).filter_by(is_active=True).all():
            bal=ledger_repo.current_balance(client.id); outstanding += bal
            if client.debt_limit and client.debt_limit > 0 and bal > client.debt_limit: over_limit += 1
        def avg(model, col): return round((self.session.query(func.count(model.id)).filter(col>=period_start).scalar() or 0)/days, 2)
        return {"today_breakfast_revenue": breakfast_revenue, "today_lunch_revenue": lunch_revenue, "today_client_payments": payments_today, "today_supplier_expenses": expenses_today, "outstanding_debt": normalize_money(outstanding), "clients_over_limit": over_limit, "recent_payments": ledger_repo.recent(LEDGER_CREDIT), "recent_charges": ledger_repo.recent(LEDGER_DEBIT), "recent_supplier_expenses": self.session.query(ManualCharge).order_by(ManualCharge.created_at.desc()).limit(5).all(), "avg_breakfast_orders": avg(BreakfastOrder, BreakfastOrder.created_at), "avg_lunch_orders": avg(LunchOrder, LunchOrder.created_at), "avg_payments": avg(Payment, Payment.created_at), "avg_supplier_expenses": avg(ManualCharge, ManualCharge.created_at), "average_period_days": days}
