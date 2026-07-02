"""User-safe error handling helpers."""

from __future__ import annotations

from flask import current_app, flash
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.i18n import _

SAFE_ERROR_KEYS = {
    'error.required', 'error.invalid_amount', 'error.delete_blocked',
    'lunch.no_menu_today', 'lunch.closed_today',
}


def friendly_error_key(exc: Exception) -> str:
    if isinstance(exc, ValueError) and str(exc) in SAFE_ERROR_KEYS:
        return str(exc)
    return 'error.generic'


def handle_form_exception(exc: Exception, action: str = 'form.error') -> None:
    """Rollback, log technical details, and flash only translated safe text."""
    db.session.rollback()
    current_app.logger.exception("%s", action, exc_info=exc)
    try:
        from app.audit import log_audit
        log_audit(action, 'Error', None, exc.__class__.__name__, severity='ERROR')
        db.session.commit()
    except Exception:
        db.session.rollback()
    flash(_(friendly_error_key(exc)), 'danger')
