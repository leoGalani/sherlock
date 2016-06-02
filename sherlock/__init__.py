"""Flask Main Project File."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, lazy_gettext

app = Flask(__name__, instance_relative_config=True)
db_relative_path = '/data/sherlock.db'
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = lazy_gettext('Access deny. Please Login')

babel = Babel(app)


from sherlock.data import model

from sherlock.controllers.users import user
from sherlock.controllers.projects import project
from sherlock.controllers.scenarios import scenario


app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(project, url_prefix='/project')
app.register_blueprint(scenario,
                       url_prefix='/project/<int:project_id>/scenario')
