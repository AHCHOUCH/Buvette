"""Routes for the dashboard feature."""

from flask import Blueprint, render_template
from flask_login import login_required

from app.dashboard.service import DashboardService


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("/")
@login_required
def index():
    """Display a temporary operational dashboard for navigation verification."""

    cards = [
        ("Clients", "0", "Client directory placeholder"),
        ("Breakfast Products", "0", "Breakfast setup placeholder"),
        ("Lunch Menus", "0", "Lunch planning placeholder"),
        ("Today's Charges", f"€{DashboardService.todays_charges():.2f}", "Charge total placeholder"),
        ("Today's Payments", f"€{DashboardService.todays_payments():.2f}", "Payment total placeholder"),
        ("Outstanding Balance", f"€{DashboardService.outstanding_balances():.2f}", "Balance placeholder"),
    ]
    return render_template("dashboard/index.html", cards=cards)
