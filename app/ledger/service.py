"""Reusable ledger services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from app.models import LedgerEntry
from app.repositories.core import LedgerRepository
from app.utils.constants import LEDGER_CREDIT, LEDGER_DEBIT
from app.utils.formatting import normalize_money


@dataclass(frozen=True)
class PreparedLedgerEntry:
    client_id: int; entry_type: str; amount: Decimal; running_balance: Decimal
    reference_type: str | None = None; reference_id: int | None = None; description: str | None = None
    timestamp: datetime | None = None; created_by_user_id: int | None = None


class LedgerService:
    VALID_ENTRY_TYPES = {LEDGER_DEBIT, LEDGER_CREDIT}
    def __init__(self, session): self.session = session; self.repo = LedgerRepository(session)

    @classmethod
    def prepare_entry(cls, *, client_id: int, entry_type: str, amount, current_balance=Decimal("0.00"), reference_type=None, reference_id=None, description=None, created_by_user_id=None, timestamp=None):
        normalized_amount = normalize_money(amount); normalized_balance = normalize_money(current_balance)
        if entry_type not in cls.VALID_ENTRY_TYPES: raise ValueError(f"Unsupported ledger entry type: {entry_type}")
        if normalized_amount < 0: raise ValueError("Ledger amount cannot be negative")
        signed_amount = normalized_amount if entry_type == LEDGER_DEBIT else -normalized_amount
        return PreparedLedgerEntry(client_id, entry_type, normalized_amount, normalize_money(normalized_balance + signed_amount), reference_type, reference_id, description, timestamp or datetime.now(timezone.utc), created_by_user_id)

    @staticmethod
    def calculate_balance(entries: list[LedgerEntry]) -> Decimal:
        balance = Decimal("0.00")
        for entry in entries: balance += entry.signed_amount()
        return normalize_money(balance)

    def post_entry(self, *, client_id, entry_type, amount, reference_type, reference_id, description, created_by_user_id=None):
        current = self.repo.current_balance(client_id)
        prepared = self.prepare_entry(client_id=client_id, entry_type=entry_type, amount=amount, current_balance=current, reference_type=reference_type, reference_id=reference_id, description=description, created_by_user_id=created_by_user_id)
        entry = LedgerEntry(**prepared.__dict__)
        self.repo.add(entry)
        return entry

    def list_entries(self, **filters): return self.repo.list(**filters)
    def recent(self, entry_type, limit=5): return self.repo.recent(entry_type, limit)
