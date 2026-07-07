"""Routes for ledger review and export."""
from datetime import date, datetime
import csv, io, re
from flask import Blueprint, Response, render_template, request
from app import db
from app.audit import log_audit
from app.permissions import permission_required
from app.clients.service import ClientService
from app.charges.service import SupplierService, CATEGORIES
from app.ledger.service import LedgerService, GlobalLedgerService
from app.settings.service import SettingsService
ledger_bp=Blueprint('ledger', __name__, url_prefix='/ledger')
def _parse_date(name):
    value=request.args.get(name) or request.args.get({'start_date':'date_from','end_date':'date_to'}.get(name,name)); return datetime.strptime(value, '%Y-%m-%d').date() if value else None
def _filters(): return {'client_id': request.args.get('client_id', type=int), 'start_date': _parse_date('start_date'), 'end_date': _parse_date('end_date'), 'reference_type': request.args.get('reference_type') or None}
def _global_filters(): return {'date_from':_parse_date('date_from'),'date_to':_parse_date('date_to'),'direction':request.args.get('type') or 'all','client_id':request.args.get('client_id', type=int),'supplier_id':request.args.get('supplier_id', type=int),'category':request.args.get('category') or None}
@ledger_bp.get('/')
@permission_required('ledger')
def index():
    mode=request.args.get('mode','client')
    clients=ClientService(db.session).list_clients(include_archived=True); suppliers=SupplierService(db.session).list_suppliers(include_archived=True)
    if mode == 'global':
        filters=_global_filters(); rows=GlobalLedgerService(db.session).rows(**filters); totals=GlobalLedgerService(db.session).totals(rows)
        return render_template('ledger/index.html', mode='global', rows=rows, totals=totals, clients=clients, suppliers=suppliers, categories=CATEGORIES, filters=filters)
    filters=_filters(); entries=LedgerService(db.session).list_entries(**filters)
    return render_template('ledger/index.html', mode='client', entries=entries, clients=clients, suppliers=suppliers, categories=CATEGORIES, filters=filters)
@ledger_bp.get('/export.csv')
@permission_required('ledger')
def export_csv():
    identity=SettingsService(db.session).identity(); output=io.StringIO(); writer=csv.writer(output)
    if request.args.get('mode') == 'global':
        rows=GlobalLedgerService(db.session).rows(**_global_filters()); writer.writerow(['Grand livre global']); writer.writerow(['Date','Sens','Catégorie','Source','Description','Montant','Créé par','Référence'])
        for r in reversed(rows): writer.writerow([r['date'].strftime('%Y-%m-%d %H:%M:%S'), 'Revenu' if r['direction']=='income' else 'Dépense', r['category'], r['source'], r['description'], f"{r['amount']:.2f}", r['created_by'], r['reference_id']])
    else:
        filters=_filters(); scope=request.args.get('scope','filtered')
        if scope == 'all': filters={'client_id':None,'start_date':None,'end_date':None,'reference_type':None}
        entries=list(reversed(LedgerService(db.session).list_entries(**filters))); writer.writerow([identity['organization_name']]); writer.writerow(['date','client employee number','client name','transaction type','description','debit','credit','running balance','created by','reference/order id'])
        for e in entries: writer.writerow([e.timestamp.strftime('%Y-%m-%d %H:%M:%S'), e.client.account_code or '', e.client.name, e.reference_type or e.entry_type, e.description or '', f"{e.amount:.2f}" if e.entry_type=='debit' else '', f"{e.amount:.2f}" if e.entry_type=='credit' else '', f"{e.running_balance:.2f}", getattr(e.created_by_user,'display_name','') or '', e.reference_id or ''])
    log_audit('ledger.export','LedgerEntry',None,'Exported ledger CSV'); db.session.commit()
    return Response('\ufeff'+output.getvalue(), mimetype='text/csv; charset=utf-8', headers={'Content-Disposition': f'attachment; filename="{_filename(identity)}"'})
def _filename(identity):
    prefix=re.sub(r'[^A-Za-z0-9_-]+','-',(identity.get('organization_short_name') or identity.get('organization_name') or 'buvette')).strip('-').lower() or 'buvette'
    return f"{prefix}-ledger-{date.today().isoformat()}.csv"
