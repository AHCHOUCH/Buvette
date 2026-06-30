"""Reusable ledger services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from app.models import LedgerEntry
from app.utils.constants import LEDGER_CREDIT, LEDGER_DEBIT
from app.utils.formatting import normalize_money


@dataclass(frozen=True)
class PreparedLedgerEntry:
    """In-memory representation of a ledger entry before persistence."""

    client_id: int
    entry_type: str
    amount: Decimal
    running_balance: Decimal
    reference_type: str | None = None
    reference_id: int | None = None
    description: str | None = None
    timestamp: datetime | None = None
    created_by_user_id: int | None = None


class LedgerService:
    """Ledger helpers shared by future charge and payment workflows."""

    VALID_ENTRY_TYPES = {LEDGER_DEBIT, LEDGER_CREDIT}

    @classmethod
    def prepare_entry(cls, *, client_id: int, entry_type: str, amount: Decimal | str | int | float,
                      current_balance: Decimal | str | int | float = Decimal("0.00"),
                      reference_type: str | None = None, reference_id: int | None = None,
                      description: str | None = None, created_by_user_id: int | None = None,
                      timestamp: datetime | None = None) -> PreparedLedgerEntry:
        """Build a ledger entry object without saving it."""

        normalized_amount = normalize_money(amount)
        normalized_balance = normalize_money(current_balance)
        if entry_type not in cls.VALID_ENTRY_TYPES:
            raise ValueError(f"Unsupported ledger entry type: {entry_type}")
        if normalized_amount < 0:
            raise ValueError("Ledger amount cannot be negative")

        signed_amount = normalized_amount if entry_type == LEDGER_DEBIT else -normalized_amount
        return PreparedLedgerEntry(
            client_id=client_id,
            entry_type=entry_type,
            amount=normalized_amount,
            running_balance=normalize_money(normalized_balance + signed_amount),
            reference_type=reference_type,
            reference_id=reference_id,
            description=description,
            timestamp=timestamp or datetime.now(timezone.utc),
            created_by_user_id=created_by_user_id,
        )

    @staticmethod
    def calculate_balance(entries: list[LedgerEntry]) -> Decimal:
        """Calculate a client balance from ledger entries."""

        balance = Decimal("0.00")
        for entry in entries:
            balance += entry.signed_amount()
        return normalize_money(balance)

    @staticmethod
    def post_entry(prepared_entry: PreparedLedgerEntry) -> LedgerEntry:
        """Future persistence interface for ledger posting workflows."""

        raise NotImplementedError("Ledger posting will be implemented with the first financial workflow")
