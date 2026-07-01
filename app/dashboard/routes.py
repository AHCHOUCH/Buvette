"""Routes for the dashboard feature."""
from flask import Blueprint, render_template, url_for
from app.permissions import permission_required, has_permission
from app import db
from app.dashboard.service import DashboardService

dashboard_bp=Blueprint('dashboard', __name__, url_prefix='/dashboard')
@dashboard_bp.get('/')
@permission_required('dashboard')
def index():
    metrics=DashboardService(db.session).metrics()
    all_actions=[('New Client', 'clients.create', 'clients'), ('Breakfast Order', 'breakfast.index', 'breakfast'), ('Lunch Charge', 'lunch.index', 'lunch'), ('Supplier Charges', 'charges.index', 'charges'), ('Payment', 'payments.index', 'payments'), ('Ledger', 'ledger.index', 'ledger')]
    actions=[(label, url_for(endpoint)) for label, endpoint, perm in all_actions if has_permission(perm)]
    return render_template('dashboard/index.html', metrics=metrics, actions=actions)
