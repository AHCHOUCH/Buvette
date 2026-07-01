"""Routes for the ledger feature."""

from flask import Blueprint, render_template
from flask_login import login_required


ledger_bp = Blueprint("ledger", __name__, url_prefix="/ledger")


@ledger_bp.get("/")
@login_required
def index():
    """Display a safe placeholder until the ledger workflow is implemented."""

    return render_template("placeholder.html", module_name="Ledger")
