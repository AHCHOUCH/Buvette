"""Routes for client management."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app import db
from app.clients.forms import ClientForm
from app.clients.service import ClientService

clients_bp=Blueprint('clients', __name__, url_prefix='/clients')
@clients_bp.get('/')
@login_required
def index():
    service=ClientService(db.session); q=request.args.get('q',''); include=request.args.get('include_archived')=='1'
    clients=service.list_clients(q, include); balances=service.balances(clients)
    warnings={c.id: service.check_debt_warning_for_balance(c, balances[c.id]) for c in clients}
    return render_template('clients/index.html', clients=clients, balances=balances, warnings=warnings, q=q, include_archived=include)
@clients_bp.route('/new', methods=['GET','POST'])
@login_required
def create():
    form=ClientForm()
    if form.validate_on_submit():
        try:
            service=ClientService(db.session); service.save_client(name=form.name.data, account_code=form.account_code.data, debt_limit=form.debt_limit.data, notes=form.notes.data, is_active=form.is_active.data)
            db.session.commit(); flash('Client saved.', 'success'); return redirect(url_for('clients.index'))
        except ValueError as exc: db.session.rollback(); flash(str(exc),'danger')
    return render_template('clients/form.html', form=form, title='New Client')
@clients_bp.route('/<int:client_id>/edit', methods=['GET','POST'])
@login_required
def edit(client_id):
    service=ClientService(db.session); client=service.find_client(client_id)
    if not client: flash('Client not found.','danger'); return redirect(url_for('clients.index'))
    form=ClientForm(obj=client)
    if form.validate_on_submit():
        try:
            service.save_client(name=form.name.data, account_code=form.account_code.data, debt_limit=form.debt_limit.data, notes=form.notes.data, is_active=form.is_active.data, client=client)
            db.session.commit(); flash('Client updated.', 'success'); return redirect(url_for('clients.index'))
        except ValueError as exc: db.session.rollback(); flash(str(exc),'danger')
    return render_template('clients/form.html', form=form, title='Edit Client')
@clients_bp.post('/<int:client_id>/archive')
@login_required
def archive(client_id):
    service=ClientService(db.session); client=service.find_client(client_id)
    if client: service.archive(client); db.session.commit(); flash('Client archived.','success')
    return redirect(url_for('clients.index'))
@clients_bp.post('/<int:client_id>/restore')
@login_required
def restore(client_id):
    service=ClientService(db.session); client=service.find_client(client_id)
    if client: service.restore(client); db.session.commit(); flash('Client restored.','success')
    return redirect(url_for('clients.index', include_archived=1))
