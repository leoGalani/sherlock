"""Load Objects to be displayed on the sherlock application."""
from flask import g
from sherlock import cache


@cache.memoize(50)
def project_loader(Project):
    """Get all projects and retrive to the global flask G."""
    g.projects = Project.query.all()


def load_cases_names_for_cycle(Scenario, Case, cycle_history):
    cases = Case.query.join(
        Scenario, Case.scenario_id == Scenario.id).filter(
            Scenario.project_id == cycle_history[0].scenario_id).all()
    scenarios = Scenario.query.filter_by(
        id=cycle_history[0].scenario_id).all()

    g.cycle_scenarios = dict()
    g.cycle_cases = dict()

    for cycle_item in cycle_history:
        for case in cases:
            if cycle_item.case_id == case.id:
                cycle_item.case_name = case.name
                g.cycle_cases[case.id] = case.name
        for scenario in scenarios:
            if cycle_item.scenario_id == scenario.id:
                g.cycle_scenarios[scenario.id] = scenario.name

    return cycle_history

def load_cycle_history(current_cycle, CycleHistory):
    if current_cycle:
        g.current_cycle = current_cycle
        g.current_cycle_history = CycleHistory.query.filter_by(
            cycle_id=current_cycle.id).all()
        g.current_cycle_history
        g.current_cycle_stats = count_cycle_stats(g.current_cycle_history)
        g.project.has_cycle = True
    else:
        g.project.has_cycle = False


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
