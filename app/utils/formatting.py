"""Formatting helpers for money, balances, and dates."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

from app.utils.constants import DEFAULT_CURRENCY

TWOPLACES = Decimal("0.01")


def normalize_money(value: Decimal | str | int | float | None) -> Decimal:
    """Convert a value to a two-decimal Decimal."""

    if value is None:
        value = Decimal("0.00")
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def format_currency(value: Decimal | str | int | float | None, currency: str = DEFAULT_CURRENCY) -> str:
    return f"{currency}{normalize_money(value):,.2f}"


def format_balance(value: Decimal | str | int | float | None, currency: str = DEFAULT_CURRENCY) -> str:
    amount = normalize_money(value)
    if amount < 0:
        return f"Credit {currency}{abs(amount):,.2f}"
    return f"Due {currency}{amount:,.2f}"


def format_date(value: date | datetime | None, pattern: str = "%d/%m/%Y") -> str:
    return "" if value is None else value.strftime(pattern)


def format_datetime(value: datetime | None, pattern: str = "%d/%m/%Y %H:%M") -> str:
    return "" if value is None else value.strftime(pattern)
