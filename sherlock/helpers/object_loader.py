"""Load Objects to be displayed on the sherlock application."""
from flask import g
from sherlock import cache


@cache.memoize(50)
def project_loader(Project):
    """Get all projects and retrive to the global flask G."""
    g.projects = Project.query.all()


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
