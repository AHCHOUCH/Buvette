"""Routes for ledger review and export."""
from datetime import date, datetime
import csv
import io
import re
from flask import Blueprint, Response, render_template, request
from app import db
from app.audit import log_audit
from app.permissions import permission_required
from app.clients.service import ClientService
from app.ledger.service import LedgerService
from app.settings.service import SettingsService

ledger_bp=Blueprint('ledger', __name__, url_prefix='/ledger')

def _filters():
    def parse(name):
        value=request.args.get(name); return datetime.strptime(value, '%Y-%m-%d').date() if value else None
    return {'client_id': request.args.get('client_id', type=int), 'start_date': parse('start_date'), 'end_date': parse('end_date'), 'reference_type': request.args.get('reference_type') or None}

@ledger_bp.get('/')
@permission_required('ledger')
def index():
    filters=_filters(); entries=LedgerService(db.session).list_entries(**filters); clients=ClientService(db.session).list_clients(include_archived=True)
    return render_template('ledger/index.html', entries=entries, clients=clients, filters=filters)

@ledger_bp.get('/export.csv')
@permission_required('ledger')
def export_csv():
    filters=_filters(); scope=request.args.get('scope','filtered')
    if scope == 'all': filters={'client_id':None,'start_date':None,'end_date':None,'reference_type':None}
    entries=list(reversed(LedgerService(db.session).list_entries(**filters)))
    identity=SettingsService(db.session).identity(); currency=identity['currency']
    output=io.StringIO(); writer=csv.writer(output)
    writer.writerow([identity['organization_name']])
    writer.writerow([f"Devise: {currency}"])
    writer.writerow(['date','client employee number','client name','transaction type','description','debit','credit','running balance','created by','reference/order id'])
    for e in entries:
        writer.writerow([e.timestamp.strftime('%Y-%m-%d %H:%M:%S'), e.client.account_code or '', e.client.name, e.reference_type or e.entry_type, e.description or '', f"{e.amount:.2f}" if e.entry_type=='debit' else '', f"{e.amount:.2f}" if e.entry_type=='credit' else '', f"{e.running_balance:.2f}", getattr(e.created_by_user, 'display_name', '') or '', e.reference_id or ''])
    log_audit('ledger.export','LedgerEntry',None,f"Exported ledger CSV ({scope})", metadata={'filters': {k: str(v) if v else '' for k,v in filters.items()}, 'rows': len(entries)})
    db.session.commit()
    filename=_filename(identity, filters, scope)
    return Response('\ufeff'+output.getvalue(), mimetype='text/csv; charset=utf-8', headers={'Content-Disposition': f'attachment; filename="{filename}"'})

def _filename(identity, filters, scope):
    prefix=identity.get('organization_short_name') or identity.get('organization_name') or 'buvette'
    prefix=re.sub(r'[^A-Za-z0-9_-]+','-',prefix).strip('-').lower() or 'buvette'
    today=date.today().isoformat()
    if scope == 'all': return f"{prefix}-ledger-complete-{today}.csv"
    start=filters.get('start_date'); end=filters.get('end_date')
    if start or end: return f"{prefix}-ledger-{start or 'start'}-to-{end or 'end'}.csv"
    return f"{prefix}-ledger-filtered-{today}.csv"
