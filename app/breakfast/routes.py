"""Routes for breakfast products and orders."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.security import check_password_hash
from app import db
from app.audit import log_audit
from app.permissions import permission_required
from app.breakfast.forms import BreakfastProductForm, ProductDeleteForm
from app.breakfast.service import BreakfastService
from app.clients.service import ClientService
from app.i18n import _
from app.utils.parsing import parse_required_int
from app.utils.errors import handle_form_exception
from app.utils.constants import ROLE_ADMIN

breakfast_bp=Blueprint('breakfast', __name__, url_prefix='/breakfast')
@breakfast_bp.route('/', methods=['GET','POST'])
@permission_required('breakfast.sell')
def index():
    svc=BreakfastService(db.session); client_svc=ClientService(db.session)
    if request.method=='POST':
        try:
            quantities={k.removeprefix('qty_'): v for k,v in request.form.items() if k.startswith('qty_')}
            svc.create_order(parse_required_int(request.form.get('client_id')), quantities, request.form.get('notes',''), getattr(current_user,'id',None)); db.session.commit(); flash(_('flash.breakfast_charged'),'success'); return redirect(url_for('breakfast.index'))
        except Exception as exc: handle_form_exception(exc, 'breakfast.order_failed')
    return render_template('breakfast/index.html', clients=client_svc.list_clients(), products=svc.products(product_types=['breakfast','drink']))
@breakfast_bp.route('/products', methods=['GET','POST'])
@permission_required('breakfast.manage')
def products():
    svc=BreakfastService(db.session); form=BreakfastProductForm()
    edit_id=request.args.get('edit', type=int); editing=svc.get_product(edit_id) if edit_id else None
    if editing and request.method=='GET':
        form.name.data=editing.name; form.price.data=editing.price; form.is_active.data=editing.is_active; form.product_type.data=editing.product_type
    if form.validate_on_submit():
        try:
            product=svc.save_product(form.name.data, form.price.data, form.is_active.data, editing, form.product_type.data)
            log_audit('product.edit' if editing else 'product.create','BreakfastProduct',product.id,f'Product {product.name} saved')
            db.session.commit(); flash(_('flash.product_saved'),'success'); return redirect(url_for('breakfast.products'))
        except Exception as exc: handle_form_exception(exc, 'form.failed')
    return render_template('breakfast/products.html', form=form, products=svc.products(False), editing=editing, delete_form=ProductDeleteForm())
@breakfast_bp.post('/products/<int:product_id>/archive')
@permission_required('breakfast.manage')
def archive_product(product_id):
    product=BreakfastService(db.session).get_product(product_id)
    if product:
        BreakfastService(db.session).archive_product(product); log_audit('product.archive','BreakfastProduct',product.id,f'Archived {product.name}'); db.session.commit(); flash(_('flash.product_saved'),'success')
    return redirect(url_for('breakfast.products'))
@breakfast_bp.post('/products/<int:product_id>/delete')
@permission_required('dangerous.delete')
def delete_product(product_id):
    form=ProductDeleteForm(); svc=BreakfastService(db.session); product=svc.get_product(product_id)
    if not product: return redirect(url_for('breakfast.products'))
    if form.validate_on_submit() and current_user.role == ROLE_ADMIN and check_password_hash(current_user.password_hash, form.password.data or ''):
        try:
            name=product.name; svc.delete_product(product); log_audit('product.delete','BreakfastProduct',product_id,f'Deleted {name}', severity='WARNING'); db.session.commit(); flash(_('flash.product_deleted'),'success')
        except ValueError as exc: db.session.rollback(); flash(_(str(exc)),'danger')
    else: flash(_('error.permission_denied'),'danger')
    return redirect(url_for('breakfast.products'))
