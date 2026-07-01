"""Payment forms."""
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
class PaymentForm(FlaskForm):
    client_id=SelectField('Client', coerce=int, validators=[DataRequired()])
    amount=DecimalField('Amount', validators=[NumberRange(min=0.01)])
    note=TextAreaField('Note', validators=[Optional(), Length(max=255)])
    submit=SubmitField('Save Payment')
