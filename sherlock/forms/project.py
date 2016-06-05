"""Form generator for Projects."""
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class new_project_form(Form):
    """WTForm for new projects."""

    name = StringField('project_name', validators=[DataRequired()])


class edit_project_form(Form):
    """WTForm for new projects."""

    name = StringField('project_name', validators=[DataRequired()])
