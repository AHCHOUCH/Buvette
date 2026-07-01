"""Routes for the breakfast feature."""

from flask import Blueprint, render_template
from flask_login import login_required


breakfast_bp = Blueprint("breakfast", __name__, url_prefix="/breakfast")


@breakfast_bp.get("/")
@login_required
def index():
    """Display a safe placeholder until the breakfast workflow is implemented."""

    return render_template("placeholder.html", module_name="Breakfast")
