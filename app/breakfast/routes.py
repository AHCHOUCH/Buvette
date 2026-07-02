"""Routes for breakfast products and orders."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from app.permissions import permission_required
from app.breakfast.forms import BreakfastProductForm
from app.breakfast.service import BreakfastService
from app.clients.service import ClientService
from app.i18n import _
from app.utils.parsing import parse_required_int
from app.utils.errors import handle_form_exception

breakfast_bp=Blueprint('breakfast', __name__, url_prefix='/breakfast')
@breakfast_bp.route('/', methods=['GET','POST'])
@permission_required('breakfast')
def index():
    svc=BreakfastService(db.session); client_svc=ClientService(db.session)
    if request.method=='POST':
        try:
            quantities={k.removeprefix('qty_'): v for k,v in request.form.items() if k.startswith('qty_')}
            svc.create_order(parse_required_int(request.form.get('client_id')), quantities, request.form.get('notes',''), getattr(current_user,'id',None)); db.session.commit(); flash(_('flash.breakfast_charged'),'success'); return redirect(url_for('breakfast.index'))
        except Exception as exc: handle_form_exception(exc, 'breakfast.order_failed')
    return render_template('breakfast/index.html', clients=client_svc.list_clients(), products=svc.products())
@breakfast_bp.route('/products', methods=['GET','POST'])
@permission_required('breakfast')
def products():
    svc=BreakfastService(db.session); form=BreakfastProductForm()
    if form.validate_on_submit():
        try: svc.save_product(form.name.data, form.price.data, form.is_active.data); db.session.commit(); flash(_('flash.product_saved'),'success'); return redirect(url_for('breakfast.products'))
        except Exception as exc: handle_form_exception(exc, 'form.failed')
    return render_template('breakfast/products.html', form=form, products=svc.products(False))
