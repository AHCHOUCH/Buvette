"""Reusable validation helpers."""

from decimal import Decimal, InvalidOperation


def is_blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def parse_decimal(value: object) -> Decimal:
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, AttributeError) as exc:
        raise ValueError("Enter a valid number") from exc


def validate_non_negative_decimal(value: object) -> Decimal:
    amount = parse_decimal(value)
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return amount
