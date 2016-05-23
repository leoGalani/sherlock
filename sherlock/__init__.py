"""Flask Main Project File."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
db_relative_path = '/data/sherlock.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://{}'.format(db_relative_path)
db = SQLAlchemy(app)

from sherlock.data import model

from sherlock.controllers.users import user
from sherlock.controllers.projects import project
from sherlock.controllers.scenarios import scenario

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(project, url_prefix='/project')
app.register_blueprint(scenario,
                       url_prefix='/project/<int:project_id>/scenario')
