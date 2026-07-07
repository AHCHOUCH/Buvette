"""Routes for the dashboard feature."""
from flask import Blueprint, render_template, url_for, request
from flask_login import current_user
from app.permissions import permission_required, has_permission
from app import db
from app.dashboard.service import DashboardService
from app.utils.constants import ROLE_ADMIN

dashboard_bp=Blueprint('dashboard', __name__, url_prefix='/dashboard')
@dashboard_bp.get('/')
@permission_required('dashboard')
def index():
    svc=DashboardService(db.session)
    if current_user.role == ROLE_ADMIN:
        metrics=svc.get_admin_dashboard(request.args.get('period','daily'))
        all_actions=[('nav.clients', 'clients.index', 'clients'), ('nav.breakfast', 'breakfast.index', 'breakfast'), ('nav.lunch', 'lunch.index', 'lunch'), ('nav.expenses', 'charges.index', 'charges'), ('nav.payments', 'payments.index', 'payments'), ('nav.ledger', 'ledger.index', 'ledger')]
        actions=[(label, url_for(endpoint)) for label, endpoint, perm in all_actions if has_permission(perm)]
        return render_template('dashboard/index.html', metrics=metrics, actions=actions, dashboard_mode='admin')
    actions=[('nav.breakfast',url_for('breakfast.index')),('nav.lunch',url_for('lunch.index')),('nav.payments',url_for('payments.index')),('charges.buvette_expenses',url_for('charges.index')),('nav.products',url_for('breakfast.products')),('nav.menus',url_for('lunch.menus'))]
    return render_template('dashboard/index.html', metrics=svc.get_cashier_dashboard(getattr(current_user,'id',None)), actions=actions, dashboard_mode='cashier')
