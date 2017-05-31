from flask import Blueprint, request, g, jsonify, abort, make_response

from sherlock import db, auth
from sherlock.data.model import Scenario, Project, Case, TestCaseSchema
from sherlock.data.model import ScenariosSchema
from sherlock.helpers.string_operations import check_none_and_blank


scenario = Blueprint('scenarios', __name__)


@scenario.url_value_preprocessor
@auth.login_required
def pre_process_scenario(endpoint, values):
    """Blueprint Object Query."""
    if 'scenario_id' in values:
        scenario_id = values.pop('scenario_id')
        g.scenario = Scenario.query.filter_by(id=scenario_id).first()
        if g.scenario is None:
            abort(make_response(jsonify(message='SCENARIO_NOT_FOUND'), 400))


@scenario.route('/scenario_n_cases/<int:scenario_id>', methods=['GET'])
@auth.login_required
def get_scenario_n_tst_cases():
    """Return Scenario and Cases."""
    schema = TestCaseSchema(many=True)
    tst_cases = schema.dump(g.scenario)
    return make_response(jsonify(scenario_id=g.scenario.id,
                                 scenario_name=g.scenario.name,
                                 cases=tst_cases))


@scenario.route('/show/<int:scenario_id>', methods=['GET'])
@auth.login_required
def get_scenario():
    """Return Testcase Info."""
    scenario_schema = ScenariosSchema(many=False)
    scenario = scenario_schema.dump(g.scenario)
    return make_response(jsonify(scenario=scenario))


@scenario.route('/new_scenario_n_cases', methods=['POST'])
@auth.login_required
def new_scenario_n_cases():
    """POST endpoint for new scenario and test cases.

    Params:
         { scenario_name: required,
           project_id: required,
           case: [cases_array required]
         }
    """
    scenario = ___create_scenario(request)
    cases = request.json.get('cases')

    for case in cases:
        if case.strip() != '' :
            db.session.add(Case(name=case, scenario_id=scenario.id))
    db.session.commit()
    return make_response(jsonify(message='SCENARIO_N_CASES_CREATED'))


@scenario.route('/new', methods=['POST'])
@auth.login_required
def new():
    """POST endpoint for new scenario.

    Params:
         { scenario_name: required,
           project_id: required,
         }
    """
    scenario = ___create_scenario(request)
    return make_response(jsonify(message='SCENARIO_CREATED'))


@scenario.route('/edit/<int:scenario_id>', methods=['POST'])
@auth.login_required
def edit():
    """POST endpoint for editing existing scenarios.

    Param:
         { "scenario_name": required }
    """
    scenario = g.scenario
    scenario_name = request.get_json().get('scenario_name')
    check_none_and_blank(scenario_name, 'scenario_name')
    scenario.name = scenario_name
    db.session.add(scenario)
    db.session.commit()

    return make_response(jsonify(message='SCENARIO_EDITED'))


def ___create_scenario(request):
    scenario_name = request.json.get('scenario_name')
    project_id = request.json.get('project_id')

    check_none_and_blank(scenario_name, 'scenario_name')
    check_none_and_blank(project_id, 'project_id')

    if not Project.query.filter_by(id=project_id).first():
        abort(make_response(jsonify(message='PROJECT_NOTFOUND'), 400))

    new_scenario = Scenario(name=scenario_name, project_id=project_id)
    db.session.add(new_scenario)
    db.session.commit()
    return new_scenario
