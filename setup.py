"""Setup script to create and populate the database."""
import sys
from sherlockapi import db
from sherlockapi.data.model import User, State

# DONT CHANGE THE CODE BELOW.
try:
    state = State.query.filter_by(code='ACTIVE').first()
except:
    state = None

if state:
    choose = input('Seems you already have configured sherlock. Do you want to wipeout the current Database? (Yes/No): ')
    while not choose in['yes','Yes','Y','y','N','n','No', 'no']:
        choose = input('Urgh.. Type yes or no to the question ;)  ')

    if choose in['yes','Yes','Y', 'y']:
        confirm = input('Are you really sure? There is no comming back from this (BACKUP!) (Yes/No): ')
        while not confirm in['yes','Yes','Y','y','N','n','No','no']:
            confirm = input('Urgh.. Type yes or no to the question ;)  ')

        if choose in['yes','Yes','Y', 'y']:
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                print('Clear table %s' % table)
                db.session.execute(table.delete())
            db.session.commit()
        else:
            print('ok then! seey!')
            sys.exit()
    else:
        print('ok then! seey!')
        sys.exit()

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


name = input('Enter the First user Name: ')
email = input('Enter the First user Email: ')
password = input('Enter the First user Password: ')

initial_user = User(name=name, email=email, password=password)
db.session.add(initial_user)
db.session.commit()

print('Hell Yeah! You are good to go!')
