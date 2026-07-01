"""Routes for application settings."""
from flask import Blueprint, flash, render_template
from flask_login import login_required
from app import db
from app.permissions import permission_required
from app.auth.service import set_password
from app.settings.forms import GeneralSettingsForm
from app.settings.service import SettingsService

settings_bp=Blueprint('settings', __name__, url_prefix='/settings')
@settings_bp.route('/', methods=['GET','POST'])
@permission_required('settings')
def index():
    svc=SettingsService(db.session); values=svc.all(); values['debt_warning_default']=float(values.get('debt_warning_default') or 0); form=GeneralSettingsForm(data=values)
    if form.validate_on_submit():
        try:
            svc.save_general(form.organization_name.data, form.debt_warning_default.data, form.currency.data)
            if form.administrator_password.data: set_password('administrator', form.administrator_password.data)
            if form.cashier_password.data: set_password('cashier', form.cashier_password.data)
            db.session.commit(); flash('Settings saved.','success')
        except ValueError as exc: db.session.rollback(); flash(str(exc),'danger')
    return render_template('settings/index.html', form=form)
