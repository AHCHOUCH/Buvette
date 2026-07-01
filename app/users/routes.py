from flask import Blueprint, flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from app import db
from app.audit import log_audit
from app.auth.service import create_user
from app.models import User
from app.permissions import permission_required
from app.utils.constants import ROLE_ADMIN, ROLE_CASHIER
users_bp=Blueprint('users', __name__, url_prefix='/users')
class UserForm(FlaskForm):
    username=StringField('Nom utilisateur', validators=[DataRequired(), Length(max=80)])
    password=PasswordField('Mot de passe', validators=[Optional(), Length(max=128)])
    full_name=StringField('Nom complet', validators=[DataRequired(), Length(max=120)])
    role=SelectField('Rôle', choices=[(ROLE_ADMIN,'Administrator'),(ROLE_CASHIER,'Cashier')])
    active=BooleanField('Actif', default=True)
    submit=SubmitField('Enregistrer')
@users_bp.route('/', methods=['GET','POST'])
@permission_required('users')
def index():
    form=UserForm()
    if form.validate_on_submit():
        try:
            user=create_user(form.username.data, form.password.data, form.full_name.data, form.role.data, form.active.data)
            log_audit('user.create','User',user.id,f'User {user.username} saved'); db.session.commit(); flash('Utilisateur enregistré.','success'); return redirect(url_for('users.index'))
        except ValueError as exc: db.session.rollback(); flash(str(exc),'danger')
    return render_template('users/index.html', form=form, users=User.query.order_by(User.username).all())
