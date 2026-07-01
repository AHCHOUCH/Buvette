"""Routes for lunch charging and menus."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from app.permissions import permission_required
from app.clients.service import ClientService
from app.lunch.forms import LunchMenuForm
from app.lunch.service import LunchService

lunch_bp=Blueprint('lunch', __name__, url_prefix='/lunch')
@lunch_bp.route('/', methods=['GET','POST'])
@permission_required('lunch')
def index():
    svc=LunchService(db.session); clients=ClientService(db.session).list_clients()
    if 'client_id' in request.form:
        try: svc.charge_today(int(request.form['client_id']), user_id=getattr(current_user,'id',None)); db.session.commit(); flash('Lunch charged.','success'); return redirect(url_for('lunch.index'))
        except Exception as exc: db.session.rollback(); flash(str(exc),'danger')
    import datetime
    today_menu=svc.repo.menu_for_weekday(datetime.date.today().weekday())
    return render_template('lunch/index.html', clients=clients, menu=today_menu)
@lunch_bp.route('/menus', methods=['GET','POST'])
@permission_required('lunch')
def menus():
    svc=LunchService(db.session); form=LunchMenuForm()
    if form.validate_on_submit():
        try: svc.save_menu(form.weekday.data, form.name.data, form.price.data, form.is_active.data); db.session.commit(); flash('Menu saved.','success'); return redirect(url_for('lunch.menus'))
        except ValueError as exc: db.session.rollback(); flash(str(exc),'danger')
    return render_template('lunch/menus.html', form=form, menus=svc.menus())
