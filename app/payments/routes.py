"""Routes for cash payments."""
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from app import db
from app.permissions import permission_required
from app.clients.service import ClientService
from app.payments.forms import PaymentForm
from app.payments.service import PaymentService
from app.i18n import _
from app.utils.errors import handle_form_exception

payments_bp=Blueprint('payments', __name__, url_prefix='/payments')
@payments_bp.route('/', methods=['GET','POST'])
@permission_required('payments')
def index():
    form=PaymentForm(); clients=ClientService(db.session).list_clients(); form.client_id.choices=[('', _('client.selector.title'))]+[(str(c.id), ((c.account_code or '—') + ' — ' + c.name)) for c in clients]
    svc=PaymentService(db.session)
    if form.validate_on_submit():
        try: svc.create_payment(form.client_id.data, form.amount.data, form.note.data, getattr(current_user,'id',None)); db.session.commit(); flash(_('flash.payment_saved'),'success'); return redirect(url_for('payments.index'))
        except Exception as exc: handle_form_exception(exc, 'form.failed')
    return render_template('payments/index.html', form=form, payments=svc.history())
