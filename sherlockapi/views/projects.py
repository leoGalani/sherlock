"""Sherlock Project Controllers and Routes."""
from flask import Blueprint, request, g, jsonify, make_response, abort
from datetime import date, datetime

from sherlockapi import db, auth

from sherlockapi.data.model import Project, User, ProjectSchema
from sherlockapi.data.model import Scenario, Cycle, CycleCases
from sherlockapi.helpers.string_operations import check_none_and_blank
from sherlockapi.helpers.util import (count_cycle_stats, get_last_cycle,
                                      get_project, get_user)

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
    """Show Project Details and last cycle Details."""
    schema = ProjectSchema(many=False)
    project = schema.dump(get_project(project_id)).data
    user = User.query.filter_by(id=project['owner_id']).first()

    scenarios = Scenario.query.filter_by(project_id=project_id).first()

    project['owner_name'] = user.name
    project['owner_email'] = user.email
    if scenarios:
        project['have_scenarios'] = True
    else:
        project['have_scenarios'] = False

    project_last_cycle = get_last_cycle(project_id)

    if project_last_cycle:
        cycle_cases_h = CycleCases.query.filter_by(
            cycle_id=project_last_cycle.id).all()
        project['have_cycles'] = True
        project['last_cycle'] = {}
        project['last_cycle']['id'] = project_last_cycle.id
        project['last_cycle']['cycle'] = project_last_cycle.cycle
        project['last_cycle']['created_at'] = datetime.strftime(project_last_cycle.created_at, '%d-%m-%Y')
        project['last_cycle']['stats'] = count_cycle_stats(cycle_cases_h)
    else:
        project['have_cycles'] = False

    return make_response(jsonify(project))


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
          project_owner: not required (id),
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
        user = get_user({'id': project_owner})
        edited_project.owner_id = user.id

    if 'type_of_project' in request.json:
        type_of_project = check_none_and_blank(request, 'type_of_project')
        edited_project.type_of_project = type_of_project

    db.session.add(edited_project)
    db.session.commit()
    return make_response(jsonify(message='PROJECT_EDITED'))
