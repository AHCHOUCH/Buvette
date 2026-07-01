"""Lightweight local Flask-Login compatibility shim for offline development."""

from __future__ import annotations

from functools import wraps
from types import SimpleNamespace

from flask import current_app, flash, redirect, request, session, url_for
from werkzeug.local import LocalProxy


def _anonymous_user():
    return SimpleNamespace(is_authenticated=False, is_anonymous=True, is_active=False, display_name="Guest", role="guest", get_id=lambda: None)


def _get_current_user():
    manager = current_app.extensions.get("login_manager")
    user_id = session.get("_user_id")
    if manager and user_id and manager._user_loader:
        user = manager._user_loader(user_id)
        if user is not None:
            return user
    return _anonymous_user()


current_user = LocalProxy(_get_current_user)


class LoginManager:
    """Minimal extension object compatible with the app's Flask-Login usage."""

    def __init__(self, app=None):
        self.login_view = None
        self.login_message = "Please log in to continue."
        self.login_message_category = "message"
        self._user_loader = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions = getattr(app, "extensions", {})
        app.extensions["login_manager"] = self

        @app.context_processor
        def _inject_current_user():
            return {"current_user": current_user}

    def user_loader(self, callback):
        self._user_loader = callback
        return callback


def login_user(user, remember=False):
    session["_user_id"] = user.get_id()
    session.permanent = bool(remember)
    return True


def logout_user():
    session.pop("_user_id", None)
    return True


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            return view(*args, **kwargs)
        manager = current_app.extensions.get("login_manager")
        if manager and manager.login_message:
            flash(manager.login_message, manager.login_message_category)
        login_view = manager.login_view if manager else "auth.login"
        return redirect(url_for(login_view, next=request.url))
    return wrapped
