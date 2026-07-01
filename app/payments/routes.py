"""Routes for the payments feature."""

from flask import Blueprint, render_template
from flask_login import login_required


payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payments_bp.get("/")
@login_required
def index():
    """Display a safe placeholder until the payments workflow is implemented."""

    return render_template("placeholder.html", module_name="Payments")
