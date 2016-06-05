"""Form generator for Users."""
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class login_form(Form):
    """WTForm for login."""

    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
