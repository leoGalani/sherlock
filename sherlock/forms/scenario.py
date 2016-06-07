"""Form generator for Projects."""
from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired, length


class new_scenario_form(Form):
    """WTForm for new projects."""

    tst_scenario = TextAreaField('tst_scenario', validators=[DataRequired(),
                                                             length(max=300)])


class edit_scenario_form(Form):
    """WTForm for new projects."""

    tst_scenario = TextAreaField('tst_scenario', validators=[DataRequired,
                                                             length(max=300)])
