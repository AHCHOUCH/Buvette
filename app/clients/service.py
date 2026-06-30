"""Reusable client account services."""

from __future__ import annotations

from decimal import Decimal

from app.models import Client
from app.ledger.service import LedgerService
from app.utils.constants import WARNING_DEBT_LIMIT
from app.utils.formatting import normalize_money


class ClientService:
    """Client helpers shared by account-facing workflows."""

    def __init__(self, session):
        self.session = session

    def find_client(self, client_id: int) -> Client | None:
        """Find a client by primary key."""

        return self.session.get(Client, client_id)

    @staticmethod
    def calculate_balance(client: Client) -> Decimal:
        """Calculate the current balance from a client's ledger entries."""

        return LedgerService.calculate_balance(list(client.ledger_entries))

    @classmethod
    def check_debt_warning(cls, client: Client) -> dict[str, object] | None:
        """Return a warning when balance exceeds the debt limit; never block."""

        balance = cls.calculate_balance(client)
        debt_limit = normalize_money(client.debt_limit)
        if debt_limit > 0 and balance > debt_limit:
            return {"code": WARNING_DEBT_LIMIT, "balance": balance, "debt_limit": debt_limit, "blocking": False}
        return None

    def activate(self, client: Client) -> Client:
        client.is_active = True
        self.session.add(client)
        return client

    def deactivate(self, client: Client) -> Client:
        client.is_active = False
        self.session.add(client)
        return client
