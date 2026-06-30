"""Date and weekday helpers."""

from datetime import date

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def weekday_name(value: date) -> str:
    return WEEKDAYS[value.weekday()]


def is_weekend(value: date) -> bool:
    return value.weekday() >= 5
