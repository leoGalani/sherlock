"""Sherlock Project Controllers and Routes."""
from flask import Blueprint, request, url_for, redirect, g

from sherlock import db
from sherlock.data.model import Project


project = Blueprint('projects', __name__)


@project.url_value_preprocessor
def get_scenario(endpoint, values):
    """Blueprint Object Query."""
    if values.pop('project_id'):
        query = Project.query.filter_by(id=values.pop('project_id'))
        g.project = query.first_or_404()


@project.route('/show/<int:project_id>', methods=['GET'])
def show():
    """Show Project Details."""
    return g.project.name


@project.route('/new', methods=['GET', 'POST'])
def new():
    """POST endpoint for new projects.

    Param:
        name(required)
        slug(required).
    """
    if request.method == 'POST':
        new_project = Project(name=request.form['project_name'],
                              slug=request.form['project_name'])
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('show', project_id=new_project.id))
    elif request.method == 'GET':
        pass
        # TODO render template of the form.


@project.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit():
    """POST endpoint for editing existing users.

    Param:
        name
        slug
    """
    if request.method == 'POST':
        edited_project = g.project
        edited_project.name = request.form['project_name']
        db.session.add(edited_project)
        db.session.commit()
        return redirect(url_for('projects.show', project_id=g.project.id))
    elif request.method == 'GET':
            pass
            # TODO render template of the form.
