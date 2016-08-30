"""Sherlock Project Controllers and Routes."""
from flask import Blueprint, request, url_for, redirect, g, render_template
from flask import flash
from flask_babel import gettext
from flask_login import login_required

from sherlock import db
from sherlock.data.model import Project, Scenario, Cycle, CycleHistory
from sherlock.forms.project import new_project_form, edit_project_form
from sherlock.helpers.util import count_cycle_stats
from sherlock.helpers.util import load_cycle_history, get_last_cycle

project = Blueprint('projects', __name__)


@project.url_value_preprocessor
def get_project(endpoint, values):
    """Blueprint Object Query."""
    if 'project_id' in values:
        g.project = Project.query.filter_by(
            id=values.pop('project_id')).first()
        g.project_cycle = get_last_cycle(Cycle, g.project.id)

        if g.project_cycle:
            g.current_cycle_history = load_cycle_history(
                g.project_cycle, CycleHistory)
            g.current_cycle_stats = count_cycle_stats(g.current_cycle_history)


@project.route('/show/<int:project_id>', methods=['GET'])
@login_required
def show():
    """Show Project Details."""
    scenarios = Scenario.query.filter_by(project_id=g.project.id)
    if scenarios.count() == 0:
        g.project.no_scenarios = True
    else:
        g.project.no_scenarios = False

    return render_template("project/show.html")


@project.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """POST endpoint for new projects.

    Param:
        name(required)
    """
    form = new_project_form()

    if form.validate_on_submit() and request.method == 'POST':
        new_project = Project(name=request.form['name'])
        db.session.add(new_project)
        db.session.commit()
        flash(gettext('Project Created!'), 'Success')
        return redirect(url_for('projects.show', project_id=new_project.id))

    return render_template("project/new.html", form=form)


@project.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit():
    """POST endpoint for editing existing users.

    Param:
        name
    """
    form = edit_project_form()

    if form.validate_on_submit() and request.method == 'POST':
        edited_project = g.project
        edited_project.name = request.form['name']
        db.session.add(edited_project)
        db.session.commit()
        flash(gettext('Sucessufly Edited!'), 'Success')
        return redirect(url_for('projects.show', project_id=g.project.id))

    return render_template("project/edit.html", form=form)
