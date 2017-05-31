from flask import Blueprint, request, g, jsonify, abort, make_response

from sherlock import db, auth
from sherlock.data.model import Scenario, Case, TestCaseSchema
from sherlock.helpers.string_operations import check_none_and_blank

test_case = Blueprint('test_cases', __name__)


@test_case.url_value_preprocessor
@auth.login_required
def pre_process_tstcases(endpoint, values):
    """Blueprint Object Query."""
    g.scenario = Scenario.query.filter_by(id=values.pop('scenario_id'))
    if not scenario:
        abort(make_response(jsonify(message='SCENARIO_NOT_FOUND'), 400))

    if 'test_case_id' in values:
        g.test_case = Case.query.filter_by(
            id=values.pop('test_case_id')).first()
        if not g.test_case:
            abort(make_response(jsonify(message='CASE_NOT_FOUND'), 400))


@test_case.route('/show/<int:test_case_id>', methods=['GET'])
@auth.login_required
def get_tstcase():
    """Return Testcase Info."""
    tstcase_schema = TestCaseSchema(many=False)
    tstcase = tstcase_schema.dump(g.test_case)
    return make_response(jsonify(tstcase=tstcase))


@test_case.route('/new', methods=['POST'])
@auth.login_required
def new():
    """POST endpoint for new scenarios.

    Param:
        {'case_name': required }
    """
    case_name = request.json.get('case_name')
    check_none_and_blank(case_name, 'case')

    db.session.add(Case(name=case_name, scenario_id=g.scenario.id))
    db.session.commit()
    return make_response(jsonify(message='CASE_CREATED'))


@test_case.route('/edit/<int:test_case_id>', methods=['POST'])
@auth.login_required
def edit():
    """POST endpoint for new scenarios.

    Param:
        {'case_name': required }
    """
    edited_tc = g.test_case
    new_case_name = request.get_json().get('case_name')
    check_none_and_blank(case_name, 'case')
    edited_tc.name = new_case_name
    db.session.add(edited_tc)
    db.session.commit()

    return make_response(jsonify(message='CASE_EDITED'))
