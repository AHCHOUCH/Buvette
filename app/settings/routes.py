"""Routes for the settings feature."""

from flask import Blueprint, render_template
from flask_login import login_required


settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.get("/")
@login_required
def index():
    """Display a safe placeholder until the settings workflow is implemented."""

    return render_template("placeholder.html", module_name="Settings")
