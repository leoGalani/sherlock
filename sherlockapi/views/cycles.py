"""Sherlock Cycles Controllers and Routes."""
from flask import Blueprint, request, g, jsonify, abort, make_response, abort
from datetime import datetime

from sherlockapi import db, auth
from sherlockapi.data.model import Scenario, Project, Case, Cycle, CycleCases
from sherlockapi.data.model import CycleScenarios, State, CycleSchema
from sherlockapi.helpers.string_operations import check_none_and_blank
from sherlockapi.helpers.util import get_scenario, get_last_cycle, count_cycle_stats
from sherlockapi.helpers.util import get_project, get_cycle, get_user

cycle = Blueprint('cycle', __name__)


@cycle.url_value_preprocessor
@auth.login_required
def cycles_url_pre_processor(endpoint, values):
    """Blueprint Object Query."""
    if request.method == 'POST':
        if request.json is None:
            abort(make_response(jsonify(message='MISSING_JSON_HEADER'), 400))


@cycle.route('/resume/<int:cycle_id>', methods=['GET'])
@auth.login_required
def get_cycle_resume(project_id, cycle_id):
    project = get_project(project_id)
    cycle = get_cycle(cycle_id, project_id)
    cycle_cases_h = CycleCases.query.filter_by(cycle_id=cycle.id).all()

    body_response = count_cycle_stats(cycle_cases_h)
    return make_response(jsonify(body_response))

@cycle.route('/close/<int:cycle_id>', methods=['POST'])
@auth.login_required
def close():
    # TODO: Check untested cases.
    """POST endpoint for closing cycles.
    Param:
        {
            reason: required,
            user_id: required
        }
    """
    project = get_project(project_id)
    cycle = get_cycle(cycle_id, project_id)

    if cycle.state_code == "CLOSED":
        return make_response(jsonify(message='CYCLE_CLOSED'))
    else:
        reason = check_none_and_blank(request, 'reason')
        user_id = check_none_and_blank(request, 'user_id')
        user = get_user(user_id)

        cycle.closed_reason = reason
        cycle.closed_by = user.id
        cycle.state_code = "CLOSED"
        cycle.closed_at = datetime.now()
        cycle.last_change = datetime.now()

        db.session.add(cycle)
        db.session.commit()
        return make_response(jsonify(message='CYCLE_CLOSED'))


@cycle.route('/new', methods=['POST'])
@auth.login_required
def create(project_id):
    """POST endpoint for new cycles.
    Param:
        {'cycle_name': required but can be empty }
    """
    project = get_project(project_id)
    project_lasty_cycle = get_last_cycle(project.id)

    if project_lasty_cycle:
        if project_lasty_cycle.state_code == "ACTIVE":
            return make_response(jsonify(message='CURRENT_CYCLE_ACTIVE'))
        cycle_number = int(project_lasty_cycle.cycle) + 1
    else:
        cycle_number = 1

    scenarios = Scenario.query.filter_by(
        project_id=project.id).filter_by(state_code='ACTIVE').all()
    cases = Case.query.join(
        Scenario, Case.scenario_id == Scenario.id).filter(
            Scenario.project_id == project.id).filter(
                Case.state_code == "ACTIVE").all()

    if len(cases) == 0:
        abort(make_response(jsonify(message='NO_TEST_SCENARIOS')))

    if request.json.get('cycle_name') == '' or request.json.get('cycle_name') is None:
        cycle_name = request.json.get('cycle_name')
    else:
        cycle_name = "Cycle Number {}".format(cycle_number)

    new_cycle = Cycle(cycle=cycle_number,
                      name= cycle_name,
                      project_id=project.id)
    db.session.add(new_cycle)
    db.session.commit()

    for scenario in scenarios:
        scenario_cycle = CycleScenarios(cycle_id=new_cycle.id,
                                        scenario_id=scenario.id)
        db.session.add(scenario_cycle)

    for case in cases:
        cyclecase = CycleCases(cycle_id=new_cycle.id,
                               case_id=case.id,
                               scenario_id=case.scenario_id)
        db.session.add(cyclecase)
    db.session.commit()

    return make_response(jsonify(message='CYCLE_CREATED', cycle_id=new_cycle.id))


@cycle.route('/get_scenarios_for_cyle/<int:cycle_id>', methods=['GET'])
@auth.login_required
def get_scenarios_for_cyle(project_id, cycle_id):
    project = get_project(project_id)
    cycle = get_cycle(cycle_id, project_id)

    cycle_scenarios_h = CycleScenarios.query.filter_by(cycle_id=cycle.id).all()
    scenarios = Scenario.query.filter_by(project_id=project_id).all()

    obj = []

    for item in cycle_scenarios_h:
        for scenario in scenarios:
            if scenario.id == item.scenario_id :
                cases = CycleCases.query.filter_by(cycle_id=cycle.id).filter_by(scenario_id=scenario.id)
                temp = {}
                temp['scenario_name'] = scenario.name
                temp['scenario_id'] = scenario.id
                temp['scenario_cycle_id'] = item.id
                temp['cases_stats'] = count_cycle_stats(cases)
                obj.append(temp)
                break
    return make_response(jsonify(obj))

@cycle.route('/get_cases_for_cyle/<int:cycle_id>/scenario/<int:scenario_id>', methods=['GET'])
@auth.login_required
def get_cases_for_cyle(project_id, cycle_id, scenario_id):
    project = get_project(project_id)
    scenario = get_scenario(scenario_id)
    cycle = get_cycle(cycle_id, project_id)

    cycle_cases_h = CycleCases.query.filter_by(cycle_id=cycle.id).all()
    cases = Case.query.filter_by(scenario_id=scenario.id)

    obj = []
    for item in cycle_cases_h:
        for case in cases:
            if item.case_id == case.id:
                temp = {}
                temp['case_name'] = case.name
                temp['case_id'] = case.id
                temp['case_cycle_id'] = item.id
                temp['case_cycle_state'] = item.state_code
                obj.append(temp)
                break

    return make_response(jsonify(scenario_name=scenario.name,
                                 scenario_id=scenario.id,
                                 cycle_id=cycle.id,
                                 cases=obj))


@cycle.route('/change_case_state_code', methods=['POST'])
@auth.login_required
def change_cycle_case_state_code_(project_id):
    """ Endpoint for changing the cycle cases state_code .
    Param:
        {
            'cycle_id': required,
            'case_id': required,
            'action': required
        }
    """
    action = check_none_and_blank(request, 'action')
    case_id = check_none_and_blank(request, 'case_id')
    cycle_id = check_none_and_blank(request, 'cycle_id')
    cycle = get_cycle(cycle_id, project_id)

    last_cycle = get_last_cycle(project_id)

    if cycle.id != last_cycle.id:
        return make_response(jsonify(message='NOT_LAST_CYCLE'), 400)

    state = State.query.filter_by(code=action).first()
    if not state:
        return make_response(jsonify(message='ACTION_UNKNOW'), 400)

    edited_cycle_case = CycleCases.query.filter_by(
        cycle_id=cycle.id).filter_by(case_id=case_id).first()

    if edited_cycle_case is None:
        abort(make_response(jsonify(message='UNKNOW_CASE'), 400))
    edited_cycle_case.state_code = action
    db.session.add(edited_cycle_case)
    db.session.commit()

    return make_response(jsonify(message='CYCLE_EDITED'))
