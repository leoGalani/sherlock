"""Sherlock Cycles Controllers and Routes."""
from flask import Blueprint, request, url_for, redirect, g, flash
from flask import render_template
from flask_login import login_required
from flask_babel import gettext


from sherlock import db
from sherlock.data.model import Scenario, Project, Case, Cycle, CycleHistory
from sherlock.helpers.string_operations import is_empty


cycle = Blueprint('cycle', __name__)


@cycle.url_value_preprocessor
@login_required
def get_cycles(endpoint, values):
    """Blueprint Object Query."""
    project = Project.query.filter_by(id=values['project_id']).one()
    g.project = project

    if 'cycle_id' in values:
        g.cycle = Cycle.query.filter_by(
            project_id=values['cycle_id']).first_or_404()

        g.current_cycle = Cycle.query.filter_by(
            id=g.cycle.id).first()
    else:
        g.current_cycle = Cycle.query.order_by(
            '-id').filter_by(project_id=values.pop('project_id')).first()

    if g.current_cycle and g.current_cycle.state_code == "CLOSED":
            g.current_cycle_status_open = False
    else:
        g.current_cycle_status_open = True


@cycle.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':

        if g.current_cycle_status_open:
            flash(gettext('Close the current cycle first'), 'danger')
            return redirect(url_for('projects.show', project_id=g.project.id))

        cases = Case.query.join(
            Scenario, Case.scenario_id == Scenario.id).filter(
                Scenario.project_id == g.project.id).filter(Case.state_id == 1)

        if cases.count() == 0:
            flash(gettext('You dont have any Test Cases or Scenarios '
                          'to create a cycle'), 'danger')
            return redirect(url_for('projects.show', project_id=g.project.id))

        if g.current_cycle:
            cycle_number = int(g.current_cycle.number) + 1
        else:
            cycle_number = 1

        new_cycle = Cycle(
            number=cycle_number, project_id=g.project.id)
        db.session.add(new_cycle)
        db.session.commit()

        for case in cases:
            item = CycleHistory(cycle_id=new_cycle.id, case_id=case.id,
                                scenario_id=case.scenario_id)
            db.session.add(item)
            db.session.commit()


@cycle.route('/show/<int:cycle_id>', methods=['GET'])
@login_required
def show():
    return render_template("cycle/show.html")
