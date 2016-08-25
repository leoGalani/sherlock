"""Load Objects to be displayed on the sherlock application."""
from flask import g
from sherlock import cache


@cache.memoize(50)
def project_loader(Project):
    """Get all projects and retrive to the global flask G."""
    g.projects = Project.query.all()


def load_cycles(Project, Cycle, CycleHistory):

    g.project_current_cycle = Cycle.query.order_by(
        '-id').filter_by(project_id=Project.id).first()

    if g.project_current_cycle:
        g.current_cycle_history = CycleHistory.query.filter_by(
            cycle_id=g.current_cycle.id).all()
        g.current_cycle_history = count_cycle_stats(g.current_cycle_history)
        g.project.has_cycle = True
    else:
        g.project.has_cycle = False


def count_cycle_stats(current_cycle_history):
    NOT_EXECUTED, ERROR, BLOCKED, PASSED = 0, 0, 0, 0
    for item in current_cycle_history:
        if item.status_code == "NOT_EXECUTED":
            NOT_EXECUTED += 1
        elif item.status_code == "ERROR":
            ERROR += 1
        elif item.status_code == "BLOCKED":
            BLOCKED += 1
        elif item.status_code == "PASSED":
            PASSED += 1

    current_cycle_history.total_not_executed = NOT_EXECUTED
    current_cycle_history.total_error = ERROR
    current_cycle_history.total_blocked = BLOCKED
    current_cycle_history.total_passed = PASSED

    return current_cycle_history
