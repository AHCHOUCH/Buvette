"""Routes for the dashboard feature."""
from flask import Blueprint, render_template, url_for
from flask_login import login_required
from app import db
from app.dashboard.service import DashboardService

dashboard_bp=Blueprint('dashboard', __name__, url_prefix='/dashboard')
@dashboard_bp.get('/')
@login_required
def index():
    metrics=DashboardService(db.session).metrics()
    actions=[('New Client', url_for('clients.create')), ('Breakfast Order', url_for('breakfast.index')), ('Lunch Charge', url_for('lunch.index')), ('Manual Charge', url_for('charges.index')), ('Payment', url_for('payments.index')), ('Ledger', url_for('ledger.index'))]
    return render_template('dashboard/index.html', metrics=metrics, actions=actions)
