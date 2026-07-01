"""Routes for manual charges."""
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from app import db
from app.charges.forms import ManualChargeForm
from app.charges.service import ChargeService
from app.clients.service import ClientService

charges_bp=Blueprint('charges', __name__, url_prefix='/charges')
@charges_bp.route('/', methods=['GET','POST'])
@login_required
def index():
    form=ManualChargeForm(); clients=ClientService(db.session).list_clients(); form.client_id.choices=[(c.id,c.name) for c in clients]
    if form.validate_on_submit():
        try: ChargeService(db.session).create_charge(form.client_id.data, form.amount.data, form.category.data, form.notes.data, getattr(current_user,'id',None)); db.session.commit(); flash('Manual charge saved.','success'); return redirect(url_for('charges.index'))
        except ValueError as exc: db.session.rollback(); flash(str(exc),'danger')
    return render_template('charges/index.html', form=form)
