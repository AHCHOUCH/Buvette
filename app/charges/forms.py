"""Manual charge forms."""
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.charges.service import CATEGORIES
class ManualChargeForm(FlaskForm):
    client_id=SelectField('Client', coerce=int, validators=[DataRequired()])
    amount=DecimalField('Amount', validators=[NumberRange(min=0.01)])
    category=SelectField('Category', choices=[(c,c) for c in CATEGORIES])
    notes=TextAreaField('Notes', validators=[Optional(), Length(max=255)])
    submit=SubmitField('Save Charge')
