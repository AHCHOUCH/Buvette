"""Routes for the charges feature."""

from flask import Blueprint, render_template
from flask_login import login_required


charges_bp = Blueprint("charges", __name__, url_prefix="/charges")


@charges_bp.get("/")
@login_required
def index():
    """Display a safe placeholder until the charges workflow is implemented."""

    return render_template("placeholder.html", module_name="Charges")
