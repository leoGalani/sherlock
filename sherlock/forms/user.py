"""Form generator for Users."""
from flask_babel import gettext
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class login_form(Form):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class signup_form(Form):
    email = StringField('email', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    password = StringField('password', validators=[
            DataRequired(),
            EqualTo('confirm_password',
                    message=gettext('Passwords Must Match'))])
    confirm_password = StringField('confirm password',
                                   validators=[DataRequired()])

class edit_user_form(Form):
    email = StringField('email')
    name = StringField('name')
    password = StringField('password', validators=[
            EqualTo('confirm_password',
                    message=gettext('Passwords Must Match'))])
    confirm_password = StringField('confirm password')
