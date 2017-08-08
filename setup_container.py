"""Setup script to create and populate the database."""
from sherlockapi import db
from sherlockapi.data.model import User, State

# DONT CHANGE THE CODE BELOW.

db.create_all()

# general states
available_state = State(name="active", code="ACTIVE")
disable_state = State(name="disable", code="DISABLE")

# test_case_states
not_executed_state = State(name="not executed", code="NOT_EXECUTED")
passed_state = State(name="passed", code="PASSED")
error_state = State(name="error", code="ERROR")
blocked_state = State(name="blocked", code="BLOCKED")
ongoing_state = State(name="ongoing", code="ONGOING")

# scenario cycle history

# cycle states
closed_cycle = State(name="closed", code="CLOSED")

db.session.add(available_state)
db.session.add(disable_state)
db.session.add(not_executed_state)
db.session.add(passed_state)
db.session.add(error_state)
db.session.add(blocked_state)
db.session.add(closed_cycle)
db.session.add(ongoing_state)
db.session.commit()

initial_user = User(name='Admin',
                    email='admin@admin.xpto',
                    password='admin')
db.session.add(initial_user)
db.session.commit()
