"""Flask Main Project File."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, lazy_gettext
from flask_cache import Cache


app = Flask(__name__, instance_relative_config=True, static_url_path="")
db_relative_path = '/data/sherlock.db'
app.config.from_object('config')
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = lazy_gettext('Access deny. Please Login')

babel = Babel(app)

from sherlock.data import model

from sherlock.helpers.object_loader import project_loader

from sherlock.views.users import user
from sherlock.views.projects import project
from sherlock.views.scenarios import scenario
from sherlock.views.dashboard import dashboard


app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(project, url_prefix='/project')
app.register_blueprint(scenario,
                       url_prefix='/project_id/<int:project_id>/scenario')


@app.before_request
def before_request():
    project_loader(model.Project)
