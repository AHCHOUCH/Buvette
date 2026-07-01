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

    user = _USERS.get((username or "").strip().lower())
    if user and user.is_active and check_password_hash(user.password_hash, password or ""):
        return user
    return None


def get_user_by_id(user_id: str) -> DemoUser | None:
    """Load a user for Flask-Login sessions."""

    return _USERS.get(user_id)


def available_demo_users() -> tuple[str, ...]:
    """Return usernames enabled for this foundation build."""

    return tuple(_USERS.keys())
