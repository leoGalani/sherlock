from flask import Blueprint, request, jsonify, abort, make_response

from sherlockapi import db, auth
from sherlockapi.data.model import Case, TestCaseSchema
from sherlockapi.helpers.string_operations import check_none_and_blank

from sherlockapi.helpers.util import get_scenario, get_tstcase


test_case = Blueprint('test_cases', __name__)


@test_case.url_value_preprocessor
@auth.login_required
def pre_process_tstcases(endpoint, values):
    """Blueprint Object Query."""
    if request.method == 'POST':
        if request.json is None:
            abort(make_response(jsonify(message='MISSING_JSON_HEADER'), 400))


@test_case.route('/show/<int:test_case_id>', methods=['GET'])
@auth.login_required
def show_testcase(scenario_id, test_case_id):
    """Return Testcase Info."""
    tst_case = get_tstcase(test_case_id)
    tstcase_schema = TestCaseSchema(many=False)
    tstcase = tstcase_schema.dump(tst_case).data
    return make_response(jsonify(tstcase))


@test_case.route('/new', methods=['POST'])
@auth.login_required
def new(scenario_id):
    """POST endpoint for new scenarios.

    Param:
        {'case_name': required }
    """
    case_name = check_none_and_blank(request, 'case_name')

    scenario = get_scenario(scenario_id)
    case = Case(name=case_name, scenario_id=scenario.id)
    db.session.add(case)
    db.session.commit()
    return make_response(jsonify(message='CASE_CREATED'))


@test_case.route('/change_status', methods=['POST'])
@auth.login_required
def tstcase_changestatus(scenario_id):
    """POST endpoint for new scenarios.

    Param:
        {
         'case_id': required,
         'action': required,
        }

    TODO: State is not defined
    """
    case_id = check_none_and_blank(request, 'case_id')
    action = check_none_and_blank(request, 'action')
    tst_case = get_tstcase(case_id)

    if action == 'REMOVE':
        db.session.delete(tst_case)
        db.session.commit()
        return make_response(jsonify(message='TSTCASE_REMOVED'))
    elif action == 'DISABLE':
        state = State.query.filter_by(code='DISABLE').first()
    elif action == 'ENABLE':
        state = State.query.filter_by(code='ACTIVE').first()
    else:
        return make_response(jsonify(message='ACTION_UNKNOW'))

    tst_case.state = state
    db.session.add(tst_case)
    db.session.commit()
    return make_response(jsonify(message='TSTCASE_STATE_CHANGED'))


@test_case.route('/edit', methods=['POST'])
@auth.login_required
def edit(scenario_id):
    """POST endpoint for new scenarios.

    Param:
        {
         'case_name': required,
         'case_id': required
        }
    """
    case_id = check_none_and_blank(request, 'case_id')
    new_case_name = check_none_and_blank(request, 'case_name')

    edited_tc = get_tstcase(case_id)

    edited_tc.name = new_case_name
    db.session.add(edited_tc)
    db.session.commit()

    return make_response(jsonify(message='CASE_EDITED'))