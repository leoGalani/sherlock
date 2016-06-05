"""Sherlock Scenario Controllers and Routes."""
from flask import Blueprint, request, url_for, redirect, g
from flask_login import login_required

from sherlock import db
from sherlock.data.model import Scenario, Project


scenario = Blueprint('scenarios', __name__)


@scenario.url_value_preprocessor
def get_scenario(endpoint, values):
    """Blueprint Object Query."""
    if Project.query.filter_by(id=values.pop('project_id')):
        if 'scenario_id' in values:
            query = Scenario.query.filter_by(
                id=values.pop('scenario_id'))
            g.scenario = query.first_or_404()
            # Find a way to persist project_id o G


@scenario.route('/show/<int:scenario_id>', methods=['GET'])
@login_required
def show():
    """Docstring."""
    return g.scenario


@scenario.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """POST endpoint for new scenarios.

    Param:
        name(required)
        scenario_name(required).
    """
    if request.method == 'POST':
        new_scenario = Scenario(name=request.form['name'],
                                state_id=1,
                                project_id=request.form['project_id'])
        db.session.add(new_scenario)
        db.session.commit()
        return redirect(url_for('show', scenario_id=new_scenario.id))
    elif request.method == 'GET':
        pass
        # TODO return JSON.


@scenario.route('/edit/<int:scenario_id>', methods=['GET', 'POST'])
@login_required
def edit():
    """POST endpoint for editing existing scenarios.

    Param:
        name
        name
    """
    if request.method == 'POST':
        scenario = g.scenario
        scenario.name = request.form['scenario_name']

        db.session.add(scenario)
        db.session.commit()
        return redirect(url_for('scenarios.show', scenario_id=g.scenario.id))
    elif request.method == 'GET':
            pass
            # TODO render template of the form.
