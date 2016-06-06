"""Form generator for Projects."""
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, length


class new_project_form(Form):
    """WTForm for new projects."""

    name = StringField('project_name', validators=[DataRequired(),
                                                   length(max=25)])


class edit_project_form(Form):
    """WTForm for new projects."""

    name = StringField('project_name', validators=[DataRequired(),
                                                   length(max=25)])
