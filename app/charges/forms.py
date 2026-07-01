"""Supplier charge forms."""
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.charges.service import CATEGORIES
class SupplierForm(FlaskForm):
    name=StringField('Nom', validators=[DataRequired(), Length(max=160)])
    phone=StringField('Téléphone', validators=[Optional(), Length(max=80)])
    notes=TextAreaField('Notes', validators=[Optional(), Length(max=1000)])
    active=BooleanField('Actif', default=True)
    submit=SubmitField('Enregistrer')
class ManualChargeForm(FlaskForm):
    supplier_id=SelectField('Fournisseur', coerce=int, validators=[DataRequired()])
    amount=DecimalField('Montant', validators=[NumberRange(min=0.01)])
    category=SelectField('Catégorie', choices=[(c,c) for c in CATEGORIES])
    notes=TextAreaField('Notes', validators=[Optional(), Length(max=255)])
    submit=SubmitField('Enregistrer la charge')
class DeleteConfirmForm(FlaskForm):
    password=PasswordField('Mot de passe administrateur', validators=[DataRequired()])
    submit=SubmitField('Supprimer définitivement')
