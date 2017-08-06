"""Sherlock Project Controllers and Routes."""
from flask import Blueprint, request, g, jsonify, make_response, abort

from sherlockapi import db, auth
from sherlockapi.data.model import Project, Cycle, CycleHistory, User
from sherlockapi.data.model import ProjectSchema
from sherlockapi.helpers.util import count_cycle_stats
from sherlockapi.helpers.string_operations import check_none_and_blank
from sherlockapi.helpers.util import (load_cycle_history, get_last_cycle,
                                      get_project)

project = Blueprint('projects', __name__)


@project.url_value_preprocessor
@auth.login_required
def project_pre_processor(endpoint, view_args):
    """Blueprint Object Query."""
    if request.method == 'POST':
        if request.json is None:
            abort(make_response(jsonify(message='MISSING_JSON_HEADER'), 400))


@project.route('/show/<int:project_id>', methods=['GET'])
@auth.login_required
def get_project_details(project_id):
    """Show Project Details."""
    schema = ProjectSchema(many=False)
    project = schema.dump(get_project(project_id)).data
    user = User.query.filter_by(id=project['owner_id']).first()
    project['owner_name'] = user.name
    return make_response(jsonify(project))


@project.route('/show_cycle_details/<int:project_id>', methods=['GET'])
@auth.login_required
def get_project_last_cycle(project_id):
    g.project = get_project(project_id)
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
           privacy_policy: required (public or private),
           project_owner: required (current_user_id),
           type_of_project: required
         }
    """

    project_name = check_none_and_blank(request, 'project_name')
    privacy_policy = check_none_and_blank(request, 'privacy_policy')
    project_owner = check_none_and_blank(request, 'project_owner')
    type_of_project = check_none_and_blank(request, 'type_of_project')

    new_project = Project(name=project_name,
                          privacy_policy=privacy_policy,
                          owner_id=int(project_owner),
                          type_of_project=type_of_project)
    db.session.add(new_project)
    db.session.commit()

    return make_response(jsonify(message='PROJECT_CREATED'))


@project.route('/edit/<int:project_id>', methods=['POST'])
@auth.login_required
def edit(project_id):
    """POST endpoint for editing existing users.

    Param:
        { project_name: not required,
          privacy_policy: not required (public or false),
          project_owner: not required (email),
          type_of_project: not required
        }
    """
    edited_project = get_project(project_id)

    if 'project_name' in request.json:
        project_name = check_none_and_blank(request, 'project_name')
        edited_project.name = project_name

    if 'privacy_policy' in request.json:
        privacy_policy = check_none_and_blank(request, 'privacy_policy')
        edited_project.privacy_policy = privacy_policy

    if 'project_owner' in request.json:
        project_owner = check_none_and_blank(request, 'project_owner')
        user = User.query.filter_by(email=project_owner)
        edited_project.owner_id = user.id

    if 'type_of_project' in request.json:
        type_of_project = check_none_and_blank(request, 'type_of_project')
        edited_project.type_of_project = type_of_project

    db.session.add(edited_project)
    db.session.commit()
    return make_response(jsonify(message='PROJECT_EDITED'))
