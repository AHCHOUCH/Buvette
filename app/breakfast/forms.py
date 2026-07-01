"""Breakfast forms."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class BreakfastProductForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired(), Length(max=120)])
    price=DecimalField('Price', validators=[NumberRange(min=0)])
    is_active=BooleanField('Active', default=True)
    submit=SubmitField('Save Product')
