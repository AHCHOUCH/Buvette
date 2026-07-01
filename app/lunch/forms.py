"""Lunch forms."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

WEEKDAYS=[(0,'Monday'),(1,'Tuesday'),(2,'Wednesday'),(3,'Thursday'),(4,'Friday'),(5,'Saturday'),(6,'Sunday')]
class LunchMenuForm(FlaskForm):
    weekday=SelectField('Weekday', choices=WEEKDAYS, coerce=int)
    name=StringField('Menu', validators=[DataRequired(), Length(max=160)])
    price=DecimalField('Price', validators=[NumberRange(min=0)])
    is_active=BooleanField('Active', default=True)
    submit=SubmitField('Save Menu')
