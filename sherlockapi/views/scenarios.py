from flask import Blueprint, request, g, jsonify, abort, make_response

from sherlockapi import db, auth
from sherlockapi.data.model import Scenario, Project, Case, TestCaseSchema
from sherlockapi.data.model import ScenariosSchema, State
from sherlockapi.helpers.string_operations import check_none_and_blank
from sherlockapi.helpers.util import get_scenario


scenario = Blueprint('scenarios', __name__)


@scenario.url_value_preprocessor
@auth.login_required
def scenario_pre_process(endpoint, view_args):
    """Blueprint Object Query."""
    if request.method == 'POST':
        if request.json is None:
            abort(make_response(jsonify(message='MISSING_JSON_HEADER'), 400))


@scenario.route('/cases/<int:scenario_id>', methods=['GET'])
@auth.login_required
def get_scenario_n_tst_cases(scenario_id):
    """Return Scenario and Cases."""
    schema = TestCaseSchema(many=True)
    scenario = get_scenario(scenario_id)
    cases = Case.query.filter_by(scenario_id=scenario.id).all()
    tst_cases = schema.dump(cases).data

    return make_response(jsonify(scenario_id=scenario.id,
                                 scenario_name=scenario.name,
                                 cases=tst_cases))


@scenario.route('/show/<int:scenario_id>', methods=['GET'])
@auth.login_required
def show_scenario(scenario_id):
    """Return Testcase Info."""
    single_scenario = get_scenario(scenario_id)
    scenario_schema = ScenariosSchema(many=False)
    return_scenario = scenario_schema.dump(single_scenario).data
    return make_response(jsonify(return_scenario))


@scenario.route('/project_scenarios/<int:project_id>', methods=['GET'])
@auth.login_required
def get_scenarios_by_project(project_id):
    """Return Testcase Info."""

    raw_scenarios = Scenario.query.filter_by(project_id=project_id).all()
    scenario_schema = ScenariosSchema(many=True)
    scenarios = scenario_schema.dump(raw_scenarios).data
    return make_response(jsonify(scenarios))


@scenario.route('/change_status', methods=['POST'])
@auth.login_required
def remove_scenario():
    """POST endpoint for removing the scenario.

    Params:
         {
            scenario_id: required,
            action: required -> DISABLE, ACTIVE, REMOVE
         }
    """
    scenario_id = check_none_and_blank(request, 'scenario_id')
    scenario = get_scenario(scenario_id)
    action = check_none_and_blank(request, 'action')

    if action == 'REMOVE':
        db.session.delete(scenario)
        db.session.commit()
        return make_response(jsonify(message='SCENARIO_REMOVED'))
    elif action == 'DISABLE':
        state = State.query.filter_by(code='DISABLE').first()
    elif action == 'ENABLE':
        state = State.query.filter_by(code='ACTIVE').first()
    else:
        return make_response(jsonify(message='ACTION_UNKNOW'))

    scenario.state = state
    db.session.add(scenario)
    db.session.commit()
    return make_response(jsonify(message='SCENARIO_STATE_CHANGED'))


@scenario.route('/new', methods=['POST'])
@auth.login_required
def new():
    """POST endpoint for new scenario.

    Params:
         { scenario_name: required,
           project_id: required,
         }
    """
    scenario = _create_scenario(request)
    return make_response(jsonify(message='SCENARIO_CREATED'))


@scenario.route('/edit', methods=['POST'])
@auth.login_required
def edit():
    """POST endpoint for editing existing scenarios.

    Param:
         { "scenario_id": required,
           "scenario_name": required
         }
    """
    scenario_id = check_none_and_blank(request, 'scenario_id')
    scenario = get_scenario(scenario_id)
    scenario_name = check_none_and_blank(request, 'scenario_name')

    scenario.name = scenario_name
    db.session.add(scenario)
    db.session.commit()

    return make_response(jsonify(message='SCENARIO_EDITED'))


def _create_scenario(request):
    scenario_name = request.json.get('scenario_name')
    project_id = request.json.get('project_id')

    check_none_and_blank(request, 'scenario_name')
    check_none_and_blank(request, 'project_id')

    if not Project.query.filter_by(id=project_id).first():
        abort(make_response(jsonify(message='PROJECT_NOTFOUND'), 400))

    new_scenario = Scenario(name=scenario_name, project_id=project_id)
    db.session.add(new_scenario)
    db.session.commit()
    return new_scenario
