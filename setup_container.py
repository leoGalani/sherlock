"""Setup script to create and populate the database."""
from sherlockapi import db
from sherlockapi.data.model import User, SherlockSettings


db.create_all()

# SherlockSettings
open_user_register = SherlockSettings('OPEN_USER_REGISTER', 'True', 'Anyone can register?')
db.session.add(open_user_register)
db.session.commit()

initial_user = User(name='Admin',
                    email='admin@admin.xpto',
                    password='admin',
                    profile='admin')
db.session.add(initial_user)
db.session.commit()
