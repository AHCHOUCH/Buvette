"""Shared WTForms validators."""

from wtforms.validators import ValidationError

from app.utils.validation import is_blank, validate_non_negative_decimal


class NonNegativeMoney:
    """Validate that a field contains a non-negative decimal amount."""

    def __init__(self, message: str | None = None):
        self.message = message or "Enter a non-negative amount."

    def __call__(self, form, field) -> None:
        if is_blank(field.data):
            return
        try:
            field.data = validate_non_negative_decimal(field.data)
        except ValueError as exc:
            raise ValidationError(self.message) from exc
