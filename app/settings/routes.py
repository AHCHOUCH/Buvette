"""Routes for application settings."""
from pathlib import Path
from flask import Blueprint, current_app, flash, render_template
from app import db
from app.audit import log_audit
from app.i18n import _
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
            upload_root=Path(current_app.static_folder) / 'uploads'
            svc.save_general(form.data, form.logo.data, upload_root)
            if form.administrator_password.data: set_password('administrator', form.administrator_password.data)
            if form.cashier_password.data: set_password('cashier', form.cashier_password.data)
            log_audit('settings.update','Setting',None,'Updated organization settings')
            db.session.commit(); flash(_('settings.flash.saved'),'success')
        except ValueError as exc: db.session.rollback(); flash(_(str(exc)),'danger')
        except OSError:
            current_app.logger.exception('Logo upload failed')
            db.session.rollback(); flash(_('settings.error.logo_write_failed'),'danger')
    elif form.errors:
        flash(_('settings.error.validation'),'danger')
    return render_template('settings/index.html', form=form, settings_values=svc.identity())
