"""Payment forms."""
from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
class PaymentForm(FlaskForm):
    client_id=SelectField('Client', coerce=lambda v: int(v) if str(v).strip() else None, validators=[DataRequired()])
    amount=DecimalField('Montant', validators=[NumberRange(min=0.01)])
    note=TextAreaField('Notes', validators=[Optional(), Length(max=255)])
    submit=SubmitField('Enregistrer')
