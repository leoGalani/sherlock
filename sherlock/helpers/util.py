"""Load Objects to be displayed on the sherlock application."""
from flask import g
from sherlock import cache


@cache.memoize(50)
def project_loader(Project):
    """Get all projects and retrive to the global flask G."""
    g.projects = Project.query.all()


def load_cases_names_for_cycle(Scenario, Case, CycleHistory, c_cycle):
    cases = Case.query.join(
         Scenario, Case.scenario_id == Scenario.id).filter(
            Scenario.project_id == c_cycle.project_id).all()

    history = CycleHistory.query.filter_by(cycle_id=c_cycle.id).all()

    scenarios = Scenario.query.filter_by(project_id=c_cycle.project_id).all()

    cycle_history_formated = []

    for scenario in scenarios:
        cycle_scenarios = dict()
        for item in history:
            if item.scenario_id == scenario.id:
                cycle_scenarios['name'] = scenario.name
                cycle_scenarios['id'] = scenario.id
                cycle_scenarios['cases'] = []
        if cycle_scenarios:
            cycle_history_formated.append(cycle_scenarios)

    for scenario in cycle_history_formated:
        for item in history:
            cycle_cases = dict()
            for case in cases:
                if item.case_id == case.id and scenario['id'] == case.scenario_id:
                    cycle_cases['name'] = case.name
                    cycle_cases['state_code'] = item.state_code
                    cycle_cases['id'] = case.id
                    scenario['cases'].append(cycle_cases)
    return cycle_history_formated

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
    NOT_EXECUTED, ERROR, BLOCKED, PASSED = 0, 0, 0, 0
    for item in current_cycle_history:
        if item.state_code == "NOT_EXECUTED":
            NOT_EXECUTED += 1
        elif item.state_code == "ERROR":
            ERROR += 1
        elif item.state_code == "BLOCKED":
            BLOCKED += 1
        elif item.state_code == "PASSED":
            PASSED += 1

    current_cycles_stats = dict()

    current_cycles_stats['total_not_executed'] = NOT_EXECUTED
    current_cycles_stats['total_error'] = ERROR
    current_cycles_stats['total_blocked'] = BLOCKED
    current_cycles_stats['total_passed'] = PASSED
    return current_cycles_stats
