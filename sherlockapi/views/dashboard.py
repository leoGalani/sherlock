"""Sherlock User Controllers and Routes."""
from flask import Blueprint, jsonify, make_response

from sherlockapi import auth
from sherlockapi.data.model import User, Project, ProjectSchema
from sherlockapi.data.model import Cycle, CycleCases, SherlockSettings
from sherlockapi.helpers.util import (count_cycle_stats, get_last_cycle,
                                      get_project)

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/', methods=['GET'])
@auth.login_required
def home():
    schema = ProjectSchema(many=True)
    projects = schema.dump(Project.query.all()).data

    for item in projects:
        project_last_cycle = get_last_cycle(item['id'])

        item['have_cycle'] = False
        if project_last_cycle:
            item['have_cycle'] = True
            cycle_cases_h = CycleCases.query.filter_by(
                cycle_id=project_last_cycle.id).all()

            item['current_cycle'] = project_last_cycle.cycle
            item['cycle_state'] = project_last_cycle.state_code.lower()
            item['stats'] =  count_cycle_stats(cycle_cases_h)

    return make_response(jsonify(projects=projects))

@dashboard.route('/check_global_register_permission', methods=['GET'])
def check_global_register_permission():
    permission = SherlockSettings.query.filter_by(
        setting='OPEN_USER_REGISTER').first()
    return make_response(jsonify(anyone_can_register=permission.value))
