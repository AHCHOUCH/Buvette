"""Routes for the lunch feature."""

from flask import Blueprint, render_template
from flask_login import login_required


lunch_bp = Blueprint("lunch", __name__, url_prefix="/lunch")


@lunch_bp.get("/")
@login_required
def index():
    """Display a safe placeholder until the lunch workflow is implemented."""

    return render_template("placeholder.html", module_name="Lunch")
