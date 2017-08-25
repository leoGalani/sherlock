from flask import Blueprint, request, g, jsonify, abort, make_response

from sherlockapi import db, auth
from sherlockapi.data.model import Scenario, Project, Case, TestCaseSchema
from sherlockapi.data.model import ScenariosSchema, StateType
from sherlockapi.data.model import Cycle, CycleScenarios, CycleCases
from sherlockapi.helpers.string_operations import check_none_and_blank
from sherlockapi.helpers.util import get_scenario, get_last_cycle


scenario = Blueprint('scenarios', __name__)


@scenario.route('/cases/<int:scenario_id>', methods=['GET'])
@auth.login_required
def get_scenario_n_tst_cases(scenario_id):
    """Return Scenario and Cases."""
    schema = TestCaseSchema(many=True)
    scenario = get_scenario(scenario_id)
    cases = Case.query.filter_by(
        scenario_id=scenario.id).filter(Case.state_code != StateType.removed).all()
    tst_cases = schema.dump(cases).data

    return make_response(jsonify(scenario_id=scenario.id,
                                 scenario_state=scenario.state_code.value,
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
    raw_scenarios = Scenario.query.filter_by(
        project_id=project_id).filter(
            Scenario.state_code != StateType.removed).all()
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

    last_cycle = get_last_cycle(scenario.project_id)

    if action in ['DISABLE', 'ENABLE', 'REMOVE']:
        if action == 'DISABLE':
            state = StateType.disable
            cycle_state = StateType.blocked
        elif action == 'ENABLE':
            state = StateType.active
            cycle_state = StateType.not_executed
        else:
            state = StateType.remove
            cycle_state = None

        scenario_case_process(last_cycle,
                              scenario,
                              state,
                              action,
                              cycle_state)
    else:
        return make_response(jsonify(message='ACTION_UNKNOW'))

    return make_response(jsonify(message='DONE'))


@scenario.route('/new', methods=['POST'])
@auth.login_required
def new():
    """POST endpoint for new scenario.

    Params:
         { scenario_name: required,
           projectId: required,
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
    project_id = request.json.get('projectId')

    check_none_and_blank(request, 'scenario_name')
    check_none_and_blank(request, 'project_id')

    if not Project.query.filter_by(id=project_id).first():
        abort(make_response(jsonify(message='PROJECT_NOTFOUND'), 400))

    new_scenario = Scenario(name=scenario_name, project_id=project_id)
    db.session.add(new_scenario)
    db.session.commit()

    project_lasty_cycle = get_last_cycle(project_id)

    if project_lasty_cycle:
        scenario_cycle = CycleScenarios(cycle_id=project_lasty_cycle.id,
                                        scenario_id=new_scenario.id)
        db.session.add(scenario_cycle)
        db.session.commit()

    return new_scenario


def scenario_case_process(cycle, scenario, state, action, cycle_state):
    scenario_cases = Case.query.filter_by(scenario_id=scenario.id).all()

    scenario.state_code = state
    db.session.add(scenario)
    db.session.commit()
    for case in scenario_cases:
        case.state_code = state
        db.session.add(case)
        db.session.commit()

    # blocking scenario on active current_cycle
    if cycle:
        if cycle_state and cycle.state_code != StateType.closed:
            cycle_scenario = CycleScenarios.query.filter_by(
                id=cycle.id).filter_by(scenario_id=scenario.id).first()

            if not cycle_scenario:
                scenario_cycle = CycleScenarios(cycle_id=cycle.id,
                                                scenario_id=scenario.id)
                db.session.add(scenario_cycle)
                db.session.commit()

            cycle_cases = CycleCases.query.filter_by(id=cycle.id).filter_by(
                scenario_id=scenario.id).all()

            if action == 'REMOVE':
                db.session.delete(cycle_scenario)
                db.session.commit()
                for ccase in cycle_cases:
                    db.session.delete(ccase)
                    db.session.commit()
            else:
                cycle_scenario.state_code = cycle_state
                db.session.add(cycle_scenario)
                db.session.commit()

                for ccase in cycle_cases:
                    ccase.state_code = cycle_state
                    db.session.add(ccase)
                    db.session.commit()
