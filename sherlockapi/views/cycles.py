"""Sherlock Cycles Controllers and Routes."""
from flask import Blueprint, request, g, jsonify, abort, make_response, abort
from datetime import datetime

from sherlockapi import db, auth
from sherlockapi.data.model import (Scenario, Project, Case, Cycle, CycleCases,
                                    CycleScenarios, StateType, CycleSchema,
                                    TagScenario, TagScenarioSchema, TagCase,
                                    TagCaseSchema)

TagScenario
from sherlockapi.helpers.string_operations import check_none_and_blank
from sherlockapi.helpers.util import get_scenario, get_last_cycle, count_cycle_stats
from sherlockapi.helpers.util import get_project, get_cycle, get_user

cycle = Blueprint('cycle', __name__)


@cycle.route('/timeline/<int:cycle_limit>', methods=['GET'])
@cycle.route('/timeline', methods=['GET'])
@auth.login_required
def get_cycle_timeline_resume(project_id, cycle_limit=7):
    # TODO: Need to find a better way - Did this cz chartist works like that.

    project = get_project(project_id)
    project_cycles = Cycle.query.filter_by(
        project_id=project.id).order_by(Cycle.id.desc()).limit(cycle_limit).all()

    cycles = []
    cycle_cases_passed = []
    cycle_cases_failed = []
    cycle_cases_blocked = []
    cycle_cases_not_executed = []

    for item in reversed(project_cycles):
        cycle_cases = CycleCases.query.filter_by(cycle_id=item.id).all()
        stats = count_cycle_stats(cycle_cases)
        if item.cycle == project_cycles[0].cycle:
            cycles.append('Current Cycle')
        else:
            if item.name == "":
                cycles.append('Cycle Number {}'.format(item.cycle))
            else:
                cycles.append(item.name)
        cycle_cases_passed.append(stats['total_passed'])
        cycle_cases_failed.append(stats['total_error'])
        cycle_cases_blocked.append(stats['total_blocked'])
        cycle_cases_not_executed.append(stats['total_not_executed'])

    return make_response(jsonify(cycles_number=cycles,
                                 cycles_passed=cycle_cases_passed,
                                 cycles_failed=cycle_cases_failed,
                                 cycles_blocked=cycle_cases_blocked,
                                 cycles_not_executed=cycle_cases_not_executed))


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
def close(project_id, cycle_id):
    # TODO: Check untested cases.
    """POST endpoint for closing cycles.
    Param:
        {
            reason: required,
        }
    """
    project = get_project(project_id)
    cycle = get_cycle(cycle_id, project_id)

    if cycle.state_code == StateType.closed:
        return make_response(jsonify(message='CYCLE_CLOSED'))
    else:
        reason = check_none_and_blank(request, 'reason')
        user = g.user

        cycle.closed_reason = reason
        cycle.closed_by = user.id
        cycle.state_code = StateType.closed
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
        if project_lasty_cycle.state_code == StateType.active:
            return make_response(jsonify(message='CURRENT_CYCLE_ACTIVE'))
        cycle_number = int(project_lasty_cycle.cycle) + 1
    else:
        cycle_number = 1

    scenarios = Scenario.query.filter_by(
        project_id=project.id).filter_by(state_code=StateType.active).all()

    cases = Case.query.join(
        Scenario, Case.scenario_id == Scenario.id).filter(
            Scenario.project_id == project.id).filter(
                Case.state_code == StateType.active).all()

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
                cases = CycleCases.query.filter_by(
                    cycle_id=cycle.id).filter_by(scenario_id=scenario.id).all()

                scenario_tags_raw = TagScenario.query.filter_by(
                    scenario_id=scenario.id).all()
                schema = TagScenarioSchema(many=True)
                scenario_tags = schema.dump(scenario_tags_raw).data

                temp = {}
                temp['scenario_name'] = scenario.name
                temp['scenario_id'] = scenario.id
                temp['scenario_cycle_id'] = item.id
                temp['cases_stats'] = count_cycle_stats(cases)
                temp['tags'] = scenario_tags

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
                cases_tags_raw = TagCase.query.filter_by(
                    case_id=case.id).all()
                schema = TagCaseSchema(many=True)
                case_tags = schema.dump(cases_tags_raw).data

                temp = {}
                temp['case_name'] = case.name
                temp['case_id'] = case.id
                temp['case_cycle_id'] = item.id
                temp['case_cycle_state'] = item.state_code.value
                temp['tags'] = case_tags
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
        return make_response(jsonify(message='NOT_LAST_CYCLE'))

    if action not in StateType.__members__:
        return make_response(jsonify(message='ACTION_UNKNOW'))

    edited_cycle_case = CycleCases.query.filter_by(
        cycle_id=cycle.id).filter_by(case_id=case_id).first()

    if edited_cycle_case is None:
        abort(make_response(jsonify(message='UNKNOW_CASE'), 404))
    edited_cycle_case.state_code = StateType[action]
    db.session.add(edited_cycle_case)
    db.session.commit()

    return make_response(jsonify(message='CYCLE_EDITED'))
