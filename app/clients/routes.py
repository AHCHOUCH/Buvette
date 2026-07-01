"""Routes for the clients feature."""

from flask import Blueprint, render_template
from flask_login import login_required


clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


@clients_bp.get("/")
@login_required
def index():
    """Display a safe placeholder until the clients workflow is implemented."""

    return render_template("placeholder.html", module_name="Clients")
