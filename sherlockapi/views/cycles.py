"""Sherlock Cycles Controllers and Routes."""
from flask import Blueprint, request, g, jsonify, abort, make_response
from datetime import datetime

from sherlockapi import db, auth
from sherlockapi.data.model import Scenario, Project, Case, Cycle, CycleHistory
from sherlockapi.data.model import State, CycleSchema, CycleHistorySchema
from sherlockapi.helpers.util import get_last_cycle
from sherlockapi.helpers.util import load_cases_names_for_cycle
from sherlockapi.helpers.util import load_cycle_history, count_cycle_stats

cycle = Blueprint('cycle', __name__)

@cycle.url_value_preprocessor
@auth.login_required
def get_cycles(endpoint, values):
    """Blueprint Object Query."""
    if request.method is 'POST':
        if request.json is None:
            return make_response(jsonify(message='MISSING_JSON_HEADER'), 400)

    g.project = Project.query.filter_by(id=values.pop('project_id')).first()

    if g.project is None:
        abort(make_response(jsonify(message='PROJECT_NOT_FOUND'), 400))

    if 'cycle_id' in values:
        g.project_cycle = Cycle.query.filter_by(
            id=values.pop('cycle_id')).filter_by(
                project_id=g.project.id).first()
        if g.project_cycle is None:
            abort(make_response(jsonify(message='CYCLE_NOT_FOUND'), 400))


@cycle.route('/close/<int:cycle_id>', methods=['POST'])
@auth.login_required
def close():
    #TODO: Check untested cases.

        """POST endpoint for closing cycles.
        Param:
            {'reason': required  }
        """

    if g.project_cycle.state_code == "CLOSED":
        return make_response(jsonify(message='CYCLE_CLOSED'))
    else:

        g.project_cycle.closed_reason = request.json.get('reason')
        g.project_cycle.closed_by = g.user.id

        g.project_cycle.state_code = "CLOSED"
        g.project_cycle.closed_at = datetime.now()
        g.project_cycle.last_change = datetime.now()

        db.session.add(g.project_cycle)
        db.session.commit()
        return make_response(jsonify(message='CYCLE_CLOSED'))


@cycle.route('/new', methods=['POST'])
@auth.login_required
def create():
    """POST endpoint for new cycles.
    Param:
        {'cycle_name': required but can be empty }
    """
    project_lasty_cycle = get_last_cycle(Cycle, g.project.id)

    if project_lasty_cycle:
        if project_lasty_cycle.state_code == "ACTIVE":
            return make_response(jsonify(message='CURRENT_CYCLE_ACTIVE'), 400)
        cycle_number = int(get_last_cycle.cycle) + 1
    else:
        cycle_number = 1

    cases = Case.query.join(
        Scenario, Case.scenario_id == Scenario.id).filter(
            Scenario.project_id == g.project.id).filter(
                Case.state_code == "ACTIVE").all()

    if len(cases) == 0:
        abort(make_response(jsonify(message='NO_TEST_SCENARIOS'), 400))

    if request.json.get('cycle_name') is not None:
        cycle_name = request.json.get('cycle_name')
    else:
        cycle_name = "Cycle Number {}".format(cycle_number)

    new_cycle = Cycle(cycle=cycle_number,
                      name= cycle_name,
                      project_id=g.project.id)
    db.session.add(new_cycle)

    for case in cases:
        item = CycleHistory(cycle_id=new_cycle.id,
                            case_id=case.id,
                            scenario_id=case.scenario_id)
        db.session.add(item)

    db.session.commit()
    return make_response(jsonify(message='CYCLE_CREATED'))


@cycle.route('/show/<int:cycle_id>', methods=['GET'])
@auth.login_required
def show():
    chistory = load_cases_names_for_cycle(
        Scenario, Case, CycleHistory, g.project_cycle)

    cycle_schema = CycleSchema(many=False)
    cycle_history_schema = CycleHistorySchema(many=Trye)

    cycle = cycle_schema.dump(g.project_cycle).data
    cycle_history = cycle_history_schema.dump(chistory).data
    return make_response(jsonify(cycle_info=cycle, cycle_history=cycle_history))


@cycle.route('/get_states/<int:cycle_id>', methods=['GET'])
@auth.login_required
def get_cycle_cases_states_count():
    cycle_history = CycleHistory.query.filter_by(
        cycle_id=g.project_cycle.id)
    count = count_cycle_stats(cycle_history)
    return jsonify({"total_error": count['total_error'],
                    "total_passed": count['total_passed'],
                    "total_blocked": count['total_blocked'],
                    "total_not_executed": count['total_not_executed']})


@cycle.route('/edit/<int:cycle_id>', methods=['POST'])
@auth.login_required
def change_case_status_for_cycle_history():

    state_code = request.get_json().get('state_code')
    case_id = request.get_json().get('case_id')

    if State.query.filter_by(code=state_code).first() is None:
        abort(make_response(jsonify(message='INCORRECT_STATUS'), 400))

    edited_cycle_case = CycleHistory.query.filter_by(
        cycle_id=g.project_cycle.id).filter_by(case_id=case_id).first()

    if edited_cycle_case is None:
        abort(make_response(jsonify(message='UNKNOW_CASE'), 400))
    edited_cycle_case.state_code = state_code
    db.session.add(edited_cycle_case)
    db.session.commit()

    return make_response(jsonify(message='CYCLE_EDITED'))
