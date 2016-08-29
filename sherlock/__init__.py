"""Flask Main Project File."""
from flask import Flask, redirect, url_for, request, flash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, lazy_gettext, gettext
from flask_cache import Cache
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__, instance_relative_config=True, static_url_path="")
db_relative_path = '/data/sherlock.db'
app.config.from_object('config')
db = SQLAlchemy(app)
CsrfProtect(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = lazy_gettext('Access deny. Please Login')

babel = Babel(app)

from sherlock.data import model

from sherlock.helpers.util import project_loader

from sherlock.views.users import user
from sherlock.views.projects import project
from sherlock.views.scenarios import scenario
from sherlock.views.dashboard import dashboard
from sherlock.views.testcases import test_case
from sherlock.views.cycles import cycle


app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(project, url_prefix='/project')
app.register_blueprint(scenario,
                       url_prefix='/project/<int:project_id>/scenario')
app.register_blueprint(cycle,
                       url_prefix='/project/<int:project_id>/cycle')
app.register_blueprint(test_case,

                       url_prefix='/scenario/<int:scenario_id>/tst_case')

@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('users.login'))


@app.errorhandler(404)
def page_not_found(error):
    flash(gettext('Route not found: {}'.format(request.path)), 'danger')

    return redirect(url_for('dashboard.home'))


@app.before_request
def before_request():
    project_loader(model.Project)
