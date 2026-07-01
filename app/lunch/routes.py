"""Routes for lunch charging and weekly menus."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from app import db
from app.permissions import permission_required
from app.clients.service import ClientService
from app.lunch.forms import LunchMenuForm
from app.lunch.service import LunchService, week_start_for
from app.i18n import _

lunch_bp=Blueprint('lunch', __name__, url_prefix='/lunch')
@lunch_bp.route('/', methods=['GET','POST'])
@permission_required('lunch.sell')
def index():
    svc=LunchService(db.session); clients=ClientService(db.session).list_clients(); plates=svc.todays_plates()
    if 'client_id' in request.form:
        try:
            svc.charge_today(int(request.form['client_id']), request.form.get('plate_id'), request.form.get('variant_id'), user_id=getattr(current_user,'id',None)); db.session.commit(); flash(_('flash.lunch_charged'),'success'); return redirect(url_for('lunch.index'))
        except Exception as exc: db.session.rollback(); flash(_(str(exc)),'danger')
    return render_template('lunch/index.html', clients=clients, plates=plates, recent_clients=clients[:6])
@lunch_bp.route('/menus', methods=['GET','POST'])
@permission_required('lunch.manage')
def menus():
    svc=LunchService(db.session); form=LunchMenuForm()
    if request.method == 'POST' and request.form.get('action') == 'create_week':
        try: svc.create_week(request.form.get('week_start_date'), request.form.get('label','')); db.session.commit(); flash(_('flash.menu_saved'),'success'); return redirect(url_for('lunch.menus'))
        except Exception as exc: db.session.rollback(); flash(_(str(exc)),'danger')
    if request.method == 'POST' and request.form.get('action') == 'copy_previous':
        try: svc.copy_previous_week(request.form.get('week_start_date')); db.session.commit(); flash(_('flash.menu_copied'),'success'); return redirect(url_for('lunch.menus'))
        except Exception as exc: db.session.rollback(); flash(_(str(exc)),'danger')
    if request.method == 'POST' and request.form.get('action') == 'add_plate':
        try: svc.add_plate(int(request.form['daily_menu_id']), request.form.get('name',''), request.form.get('description','')); db.session.commit(); flash(_('flash.menu_saved'),'success'); return redirect(url_for('lunch.menus'))
        except Exception as exc: db.session.rollback(); flash(_(str(exc)),'danger')
    return render_template('lunch/menus.html', form=form, weekly_menus=svc.menus(), today_week_start=week_start_for().isoformat())
