"""Settings forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import DecimalField, HiddenField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp

HEX = r"^#[0-9a-fA-F]{6}$"
class GeneralSettingsForm(FlaskForm):
    organization_name=StringField('settings.organization_name', validators=[DataRequired(), Length(max=120)])
    organization_short_name=StringField('settings.short_name', validators=[Optional(), Length(max=40)])
    logo_path=HiddenField()
    logo=FileField('settings.logo', validators=[FileAllowed(['png','jpg','jpeg','webp','svg'], 'settings.error.invalid_logo')])
    primary_color=StringField('settings.primary_color', validators=[DataRequired(), Regexp(HEX, message='settings.error.invalid_color')])
    secondary_color=StringField('settings.secondary_color', validators=[Optional(), Regexp(HEX, message='settings.error.invalid_color')])
    accent_color=StringField('settings.accent_color', validators=[Optional(), Regexp(HEX, message='settings.error.invalid_color')])
    header_background_color=StringField('settings.header_background_color', validators=[DataRequired(), Regexp(HEX, message='settings.error.invalid_color')])
    sidebar_background_color=StringField('settings.sidebar_background_color', validators=[DataRequired(), Regexp(HEX, message='settings.error.invalid_color')])
    button_color=StringField('settings.button_color', validators=[DataRequired(), Regexp(HEX, message='settings.error.invalid_color')])
    login_background_color=StringField('settings.login_background_color', validators=[Optional(), Regexp(HEX, message='settings.error.invalid_color')])
    footer_text=StringField('settings.footer_text', validators=[Optional(), Length(max=180)])
    debt_warning_default=DecimalField('settings.debt_warning_default', validators=[NumberRange(min=0)])
    currency=StringField('settings.currency', validators=[DataRequired(), Length(max=5)])
    administrator_password=PasswordField('settings.administrator_password', validators=[Optional(), Length(min=4, max=128)])
    cashier_password=PasswordField('settings.cashier_password', validators=[Optional(), Length(min=4, max=128)])
    submit=SubmitField('button.save')
