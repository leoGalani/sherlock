"""Load Objects to be displayed on the sherlock application."""
from flask import g, abort, make_response, jsonify

from sherlockapi.data.model import User, Project, Scenario, Case, Cycle
from sherlockapi import cache


@cache.memoize(50)
def project_loader(Project):
    """Get all projects and retrive to the global flask G."""
    g.projects = Project.query.all()


def get_last_cycle(project_id):
    cycle = Cycle.query.order_by('-id').filter_by(
        project_id=project_id).first()
    if cycle:
        return cycle
    else:
        return ''


def count_cycle_stats(casesCycle):
    current_cycles_stats = dict()
    current_cycles_stats['total_not_executed'] = 0
    current_cycles_stats['total_error'] = 0
    current_cycles_stats['total_blocked'] = 0
    current_cycles_stats['total_passed'] = 0

    for item in casesCycle:
        current_cycles_stats['total_{}'.format(item.state_code.lower())] += 1

    return current_cycles_stats


def get_user(kwargs):
    user = User.query.filter_by(**kwargs).first()
    if not user:
        abort(make_response(jsonify(message='USER_NOT_FOUND'), 404))
    else:
        return user


def get_project(user_id):
    project = Project.query.filter_by(id=user_id).first()
    if project is None:
        abort(make_response(jsonify(message='PROJECT_NOT_FOUND'), 404))
    return project


def get_scenario(scenario_id):
    scenario = Scenario.query.filter_by(id=scenario_id).first()
    if scenario is None:
        abort(make_response(jsonify(message='SCENARIO_NOT_FOUND'), 404))
    return scenario


def get_tstcase(case_id):
    test_case = Case.query.filter_by(id=case_id).first()
    if not test_case:
        abort(make_response(jsonify(message='CASE_NOT_FOUND'), 404))
    return test_case


def get_cycle(cycle_id, project_id):
    project_cycle = Cycle.query.filter_by(id=cycle_id).filter_by(
            project_id=project_id).first()
    if project_cycle is None:
        abort(make_response(jsonify(message='CYCLE_NOT_FOUND'), 404))
    return project_cycle
