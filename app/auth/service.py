"""Authentication services for Buvette Manager."""

from __future__ import annotations

from dataclasses import dataclass

from werkzeug.security import check_password_hash, generate_password_hash

from app.utils.constants import ROLE_ADMIN, ROLE_CASHIER


@dataclass(frozen=True)
class DemoUser:
    """Small login-compatible user object for foundation authentication."""

    id: str
    username: str
    display_name: str
    role: str
    password_hash: str
    active: bool = True

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_active(self) -> bool:
        return self.active

    def get_id(self) -> str:
        return self.id


_USERS = {
    "administrator": DemoUser("administrator", "administrator", "Administrator", ROLE_ADMIN, generate_password_hash("administrator")),
    "cashier": DemoUser("cashier", "cashier", "Cashier", ROLE_CASHIER, generate_password_hash("cashier")),
}


def authenticate(username: str, password: str) -> DemoUser | None:
    """Return an active user when the supplied credentials are valid."""

    key = (username or "").strip().lower()
    user = _USERS.get(key)
    password_hash = _stored_password_hash(key) or (user.password_hash if user else "")
    if user and user.is_active and check_password_hash(password_hash, password or ""):
        return user
    return None


def get_user_by_id(user_id: str) -> DemoUser | None:
    """Load a user for Flask-Login sessions."""

    return _USERS.get(user_id)


def available_demo_users() -> tuple[str, ...]:
    """Return usernames enabled for this foundation build."""

    return tuple(_USERS.keys())


def _stored_password_hash(username: str) -> str | None:
    """Read a persisted password hash when the database is available."""
    from app import db
    from app.models import Setting

    setting = db.session.get(Setting, f"password_hash_{username}")
    return setting.value if setting else None


def set_password(username: str, password: str) -> None:
    """Persist an account password hash in settings."""
    from app import db
    from app.models import Setting

    key = (username or "").strip().lower()
    if key in _USERS and password:
        setting_key = f"password_hash_{key}"
        setting = db.session.get(Setting, setting_key) or Setting(key=setting_key, value="")
        setting.value = generate_password_hash(password)
        db.session.add(setting)
