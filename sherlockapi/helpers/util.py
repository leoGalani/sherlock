"""Load Objects to be displayed on the sherlock application."""
from flask import g
from sherlockapi import cache


@cache.memoize(50)
def project_loader(Project):
    """Get all projects and retrive to the global flask G."""
    g.projects = Project.query.all()


def load_cases_names_for_cycle(Scenario, Case, CycleHistory, c_cycle):
    """Helper method so the interface can retrive the test scenarios and
    test names """

    cases = Case.query.join(
         Scenario, Case.scenario_id == Scenario.id).filter(
            Scenario.project_id == c_cycle.project_id).all()

    history = CycleHistory.query.filter_by(cycle_id=c_cycle.id).all()
    scenarios = Scenario.query.filter_by(project_id=c_cycle.project_id).all()

    for history_item in history:
        for scenario in scenarios:
            if history_item.scenario_id == scenario.id:
                history_item.scenario_name = scenario.name
                break

    for item in history:
        for case in cases:
            if history_item.case_id == case.id:
                history_item.case_name = case.name
                break

    return history

def get_last_cycle(Cycle, project_id):
    cycle = Cycle.query.order_by('-id').filter_by(
        project_id=project_id).first()
    if cycle:
        return cycle
    else:
        return False


def load_cycle_history(current_cycle, CycleHistory):
    return CycleHistory.query.filter_by(cycle_id=current_cycle.id).all()


def load_last_cyle_status_of_projects(Cycle, CycleHistory, projects):
    cyclo_stats = []
    for project in projects:
        last_cycle = get_last_cycle(Cycle, project.id)
        if last_cycle:
            cyclo_history = load_cycle_history(last_cycle, CycleHistory)
            cycle_stat = count_cycle_stats(cyclo_history)
            cycle_stat['project_id'] = project.id
            cycle_stat['project_name'] = project.name
            cycle_stat['cycle_id'] = last_cycle.id
            cycle_stat['cycle_number'] = last_cycle.number
            cycle_stat['cycle_status_code'] = last_cycle.state_code
            cyclo_stats.append(cycle_stat)
    return cyclo_stats


def count_cycle_stats(current_cycle_history):
    current_cycles_stats = dict()
    current_cycles_stats['total_not_executed'] = 0
    current_cycles_stats['total_error'] = 0
    current_cycles_stats['total_blocked'] = 0
    current_cycles_stats['total_passed'] = 0

    for item in current_cycle_history:
        current_cycles_stats['total_{}'.format(item.state_code.lower())] += 1

    return current_cycles_stats
