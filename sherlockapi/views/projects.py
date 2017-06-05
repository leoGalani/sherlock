"""Sherlock Project Controllers and Routes."""
from flask import Blueprint, request, g, jsonify, make_response

from sherlockapi import db, auth
from sherlockapi.data.model import Project, Scenario, Cycle, CycleHistory
from sherlockapi.data.model import ProjectSchema
from sherlockapi.helpers.util import count_cycle_stats
from sherlockapi.helpers.util import load_cycle_history, get_last_cycle
from sherlockapi.helpers.string_operations import check_none_and_blank

project = Blueprint('projects', __name__)


@project.url_value_preprocessor
@auth.login_required
def get_project(endpoint, values):
    """Blueprint Object Query."""
    if request.method is 'POST':
        if request.json is None:
            return make_response(jsonify(message='MISSING_JSON_HEADER'), 400)

    if 'project_id' in values:
        project_id = values.pop('project_id')
        g.project = Project.query.filter_by(id=project_id).first()
        if g.project is None:
            return make_response(jsonify(message='PROJECT_NOT_FOUND'), 404)


@project.route('/show/<int:project_id>', methods=['GET'])
@auth.login_required
def get_project_details():
    """Show Project Details."""
    schema = ProjectSchema(many=False)
    project = schema.dump(g.project).data
    return make_response(jsonify(project))


@project.route('/show_cycle_details/<int:project_id>', methods=['GET'])
@auth.login_required
def get_project_last_cycle():
    project_cycle = get_last_cycle(Cycle, g.project.id)

    if project_cycle is not None:
        current_c_history = load_cycle_history(project_cycle, CycleHistory)
        current_c_stats = count_cycle_stats(current_c_history)
        return make_response(jsonify(get_cycle="YES",
                                     stats=current_c_stats))
    else:
        return make_response(jsonify(get_cycle="NO"))


@project.route('/new', methods=['POST'])
@auth.login_required
def new():
    """POST endpoint for new projects.

    Param:
         { project_name: required,
           privacy_policy: required (public or false),
           project_owner: required (current_user_id),
           type_of_project: required
         }
    """

    project_name = request.json.get('project_name')
    privacy_policy = request.json.get('privacy_policy')
    project_owner = request.json.get('project_owner')
    type_of_project = request.json.get('type_of_project')

    check_none_and_blank(project_name, 'project_name')
    check_none_and_blank(privacy_policy, 'privacy_policy')
    check_none_and_blank(project_owner, 'project_owner')
    check_none_and_blank(type_of_project, 'type_of_project')

    new_project = Project(name=project_name,
                          privacy_policy=privacy_policy,
                          owner=project_owner,
                          type_of_project=type_of_project)
    db.session.add(new_project)
    db.session.commit()

    return make_response(jsonify(message='PROJECT_CREATED'))


@project.route('/edit/<int:project_id>', methods=[ 'POST'])
@auth.login_required
def edit():
    """POST endpoint for editing existing users.

    Param:
        { project_name: not required,
          privacy_policy: not required (public or false),
          project_owner: not required (current_user_id),
          type_of_project: not required
        }
    """
    edited_project = g.project

    project_name = request.json.get('project_name')
    privacy_policy = request.json.get('privacy_policy')
    project_owner = request.json.get('project_owner')
    type_of_project = request.json.get('type_of_project')

    if project_name:
        check_none_and_blank(project_name, 'project_name')
        edited_project.name = project_name

    if privacy_policy:
        check_none_and_blank(privacy_policy, 'privacy_policy')
        edited_project.privacy_policy = privacy_policy

    if project_owner:
        check_none_and_blank(project_owner, 'project_owner')
        edited_project.owner = project_owner

    if type_of_project:
        check_none_and_blank(type_of_project, 'type_of_project')
        edited_project.type_of_project = type_of_project

    db.session.add(edited_project)
    db.session.commit()
    return make_response(jsonify(message='PROJECT_EDITED'))
