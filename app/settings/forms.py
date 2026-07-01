"""Settings forms."""
from flask_wtf import FlaskForm
from wtforms import DecimalField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
class GeneralSettingsForm(FlaskForm):
    organization_name=StringField('Organization Name', validators=[DataRequired(), Length(max=120)])
    debt_warning_default=DecimalField('Debt Warning Default', validators=[NumberRange(min=0)])
    currency=StringField('Currency', validators=[DataRequired(), Length(max=5)])
    administrator_password=PasswordField('Administrator Password', validators=[Optional(), Length(min=4, max=128)])
    cashier_password=PasswordField('Cashier Password', validators=[Optional(), Length(min=4, max=128)])
    submit=SubmitField('Save Settings')
