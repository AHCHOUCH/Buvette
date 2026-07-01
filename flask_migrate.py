"""Lightweight local Flask-Migrate compatibility shim for offline development."""

class Migrate:
    """Minimal extension object matching the Flask-Migrate init_app API."""

    def __init__(self, app=None, db=None):
        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        app.extensions = getattr(app, "extensions", {})
        app.extensions["migrate"] = {"db": db}
