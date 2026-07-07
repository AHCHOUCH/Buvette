"""Breakfast forms."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
class BreakfastProductForm(FlaskForm):
    name=StringField('Nom', validators=[DataRequired(), Length(max=120)])
    price=DecimalField('Prix', validators=[NumberRange(min=0.01)])
    product_type=SelectField('Catégorie', choices=[('breakfast','Petit déjeuner'),('drink','Boisson'),('lunch_extra','Extra déjeuner')], default='breakfast')
    is_active=BooleanField('Actif', default=True)
    submit=SubmitField('Enregistrer')
class ProductDeleteForm(FlaskForm):
    password=PasswordField('Mot de passe administrateur', validators=[DataRequired()])
    submit=SubmitField('Supprimer définitivement')
