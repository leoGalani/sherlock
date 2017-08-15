"""Setup script to create and populate the database."""
#import random
#import string
#import yaml

#with open("docker-compose.yml", 'r') as ymlfile:
#    docker_config = yaml.load(ymlfile)

#random_db_password = ''.join(random.SystemRandom().choice(
#    string.ascii_uppercase + string.digits) for _ in range(20))

#import pdb; pdb.set_trace()

#docker_config['services']['mysql']['environment']['MYSQL_ROOT_PASSWORD'] = random_db_password

#with open("docker-compose.yml", 'w') as newconf:
#    yaml.dump(docker_config, newconf)

"""
This file changes the password from the docker-compose file,
also changing the configuration do database connection, therefore must be
applying before importing the application classes and methods.
"""

def check_first_run(db):
    db.create_all()

    from sherlockapi.data.model import User, SherlockSettings

    user = User.query.filter_by(id=1).first()
    if user == None:
        initial_user = User(name='Admin',
                            email='admin@admin.xpto',
                            password='admin',
                            profile='admin')
        db.session.add(initial_user)
        db.session.commit()

    # SherlockSettings
    open_register_setting = SherlockSettings.query.filter_by(setting='OPEN_USER_REGISTER').first()
    if not open_register_setting:
        open_user_register = SherlockSettings('OPEN_USER_REGISTER', 'True', 'Anyone can register?')
        db.session.add(open_user_register)
        db.session.commit()
