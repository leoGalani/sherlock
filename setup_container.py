"""Setup script to create and populate the database."""
import os
import yaml

with open("docker-compose.yml", 'r') as ymlfile:
    docker_config = yaml.load(ymlfile)

random_db_password = os.urandom(25)
docker_config['services']['mysql']['environment']['MYSQL_ROOT_PASSWORD'] = random_db_password

with open("docker-compose.yml", 'w') as newconf:
    yaml.dump(docker_config, newconf)

"""
This file changes the password from the docker-compose file,
also changing the configuration do database connection, therefore must be
applying before importing the application classes and methods.
"""
# the


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
