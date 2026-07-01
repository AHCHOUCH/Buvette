"""Reusable client account services."""

from __future__ import annotations
from decimal import Decimal
from app.models import Client
from app.repositories.core import ClientRepository, LedgerRepository
from app.utils.constants import WARNING_DEBT_LIMIT
from app.utils.formatting import normalize_money


class ClientService:
    def __init__(self, session): self.session=session; self.repo=ClientRepository(session); self.ledger=LedgerRepository(session)
    def list_clients(self, q="", include_archived=False): return self.repo.list(q, include_archived)
    def find_client(self, client_id: int): return self.repo.get(client_id)
    def balances(self, clients): return {c.id: normalize_money(self.ledger.current_balance(c.id)) for c in clients}
    def balance(self, client): return normalize_money(self.ledger.current_balance(client.id)) if client and client.id else Decimal("0.00")
    def save_client(self, *, name, account_code, debt_limit, notes, is_active=True, client=None):
        name=(name or "").strip(); account_code=(account_code or "").strip() or None
        if not account_code and not client:
            max_id = (self.session.query(Client.id).order_by(Client.id.desc()).first() or [0])[0] or 0
            account_code = f"EMP-{max_id + 1:04d}"
        if not name: raise ValueError("Client name is required.")
        if account_code and self.repo.find_duplicate_identifier(account_code, getattr(client, 'id', None)): raise ValueError("Another active client already uses this employee number.")
        client = client or Client()
        client.name=name; client.account_code=account_code; client.debt_limit=normalize_money(debt_limit or 0); client.notes=notes; client.is_active=is_active
        self.repo.save(client); return client
    @staticmethod
    def check_debt_warning_for_balance(client, balance):
        debt_limit=normalize_money(client.debt_limit)
        if debt_limit > 0 and balance > debt_limit: return {"code": WARNING_DEBT_LIMIT, "balance": balance, "debt_limit": debt_limit, "blocking": False}
        return None
    def archive(self, client): client.is_active=False; self.repo.save(client); return client
    def restore(self, client): client.is_active=True; self.repo.save(client); return client
