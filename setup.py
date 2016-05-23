"""Setup script to create and populate the database."""
from sherlock import db
from sherlock.data.model import User, State

db.create_all()

initial_user = User(name="Sherlock", username="sherlock", password="123")

# states
available_state = State(name="available")
disable_state = State(name="disable")

# do not change the order of the itens creation
db.session.add(initial_user)
db.session.add(available_state)
db.session.add(disable_state)
db.session.commit()
