"""Routes for supplier expenses."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.security import check_password_hash
from app import db
from app.audit import log_audit
from app.charges.forms import DeleteConfirmForm, ManualChargeForm, SupplierForm
from app.charges.service import ChargeService, SupplierService
from app.permissions import permission_required
from app.i18n import _
from app.utils.errors import handle_form_exception
charges_bp=Blueprint('charges', __name__, url_prefix='/charges')
@charges_bp.route('/', methods=['GET','POST'])
@permission_required('expenses.create')
def index():
    svc=SupplierService(db.session); form=ManualChargeForm(); form.supplier_id.choices=[(s.id,s.name) for s in svc.list_suppliers()]
    if form.validate_on_submit():
        try:
            charge=ChargeService(db.session).create_charge(form.supplier_id.data, form.amount.data, form.category.data, form.notes.data, getattr(current_user,'id',None))
            log_audit('supplier_charge.create','SupplierCharge',charge.id,'Supplier expense recorded')
            db.session.commit(); flash(_('flash.charge_saved'),'success'); return redirect(url_for('charges.index'))
        except Exception as exc: handle_form_exception(exc, 'form.failed')
    
    from app.models import ManualCharge
    q=db.session.query(ManualCharge).order_by(ManualCharge.created_at.desc())
    if current_user.role != 'admin': q=q.filter(ManualCharge.created_by_user_id==getattr(current_user,'id',None)).limit(10)
    else: q=q.limit(50)
    charges=q.all()
    return render_template('charges/index.html', form=form, charges=charges)
@charges_bp.route('/suppliers', methods=['GET','POST'])
@permission_required('suppliers')
def suppliers():
    service=SupplierService(db.session); form=SupplierForm()
    if form.validate_on_submit():
        try:
            supplier=service.save(form.name.data, form.phone.data, form.notes.data, form.active.data); log_audit('supplier.create','Supplier',None,f'Supplier {supplier.name} saved')
            db.session.commit(); flash('Fournisseur enregistré.','success'); return redirect(url_for('charges.suppliers'))
        except Exception as exc: handle_form_exception(exc, 'form.failed')
    return render_template('charges/suppliers.html', form=form, suppliers=service.list_suppliers(include_archived=request.args.get('include_archived')=='1'))
@charges_bp.post('/suppliers/<int:supplier_id>/archive')
@permission_required('suppliers')
def archive_supplier(supplier_id):
    s=SupplierService(db.session).get(supplier_id)
    if s: SupplierService(db.session).archive(s); log_audit('supplier.archive','Supplier',s.id,f'Archived {s.name}'); db.session.commit(); flash('Fournisseur archivé.','success')
    return redirect(url_for('charges.suppliers'))
@charges_bp.route('/suppliers/<int:supplier_id>/delete', methods=['GET','POST'])
@permission_required('delete')
def delete_supplier(supplier_id):
    service=SupplierService(db.session); supplier=service.get(supplier_id); form=DeleteConfirmForm()
    if not supplier: return redirect(url_for('charges.suppliers'))
    if form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, form.password.data or ''): flash('Mot de passe invalide.','danger')
        else:
            try: service.delete_if_unused(supplier); log_audit('supplier.delete','Supplier',supplier_id,'Supplier deleted', severity='WARNING'); db.session.commit(); flash('Fournisseur supprimé.','success'); return redirect(url_for('charges.suppliers'))
            except ValueError as exc: db.session.rollback(); flash(str(exc),'danger')
    return render_template('confirm_delete.html', form=form, entity=supplier.name)
