"""Client forms."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ClientForm(FlaskForm):
    account_code=StringField('Employee Number', validators=[Optional(), Length(max=50)])
    name=StringField('Full Name', validators=[DataRequired(), Length(max=160)])
    debt_limit=DecimalField('Debt Limit', validators=[NumberRange(min=0)], default=0)
    is_active=BooleanField('Active', default=True)
    notes=TextAreaField('Notes', validators=[Optional(), Length(max=1000)])
    submit=SubmitField('Save Client')
