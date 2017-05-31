"""Setup script to create and populate the database."""
from sherlock import db
from sherlock.data.model import User, State

db.create_all()

# DONT CHANGE THE CODE BELOW.
initial_user = User(name="Administrador", email="admin@admin.xpto", password="admin")
available_state = State(name="active", code="ACTIVE")
db.session.add(available_state)
db.session.add(initial_user)
db.session.commit()
# DONT CHANGE THE CODE ABOVE.

# general states
disable_state = State(name="disable", code="DISABLE")

# test_case_states
not_executed_state = State(name="not executed", code="NOT_EXECUTED")
passed_state = State(name="passed", code="PASSED")
error_state = State(name="error", code="ERROR")
blocked_state = State(name="blocked", code="BLOCKED")

# cycle states
closed_cycle = State(name="closed", code="CLOSED")

db.session.add(disable_state)
db.session.add(not_executed_state)
db.session.add(passed_state)
db.session.add(error_state)
db.session.add(blocked_state)
db.session.add(closed_cycle)
db.session.commit()
