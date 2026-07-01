"""Routes for ledger review."""
from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required
from app import db
from app.clients.service import ClientService
from app.ledger.service import LedgerService

ledger_bp=Blueprint('ledger', __name__, url_prefix='/ledger')
@ledger_bp.get('/')
@login_required
def index():
    def parse(name):
        value=request.args.get(name); return datetime.strptime(value, '%Y-%m-%d').date() if value else None
    filters={'client_id': request.args.get('client_id', type=int), 'start_date': parse('start_date'), 'end_date': parse('end_date'), 'reference_type': request.args.get('reference_type') or None}
    entries=LedgerService(db.session).list_entries(**filters); clients=ClientService(db.session).list_clients(include_archived=True)
    return render_template('ledger/index.html', entries=entries, clients=clients, filters=filters)
