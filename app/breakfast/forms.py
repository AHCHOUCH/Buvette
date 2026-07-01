"""Breakfast forms."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class BreakfastProductForm(FlaskForm):
    name=StringField('Nom', validators=[DataRequired(), Length(max=120)])
    price=DecimalField('Prix', validators=[NumberRange(min=0)])
    is_active=BooleanField('Actif', default=True)
    submit=SubmitField('Enregistrer')
