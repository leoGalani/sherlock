"""Flask Main Project File."""
from flask import Flask, request, abort, jsonify, abort, make_response, g
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_cache import Cache

app = Flask(__name__, instance_relative_config=True, static_url_path="")
CORS(app, resources={r'/*': {"origins": '*', 'allow_headers': '*'}})
app.config['CORS_HEADER'] = 'Content-Type'

db_relative_path = '/data/sherlock.db'
app.config.from_object('config')
secretkey = app.config['SECRET_KEY']
token_timeout = app.config['TOKEN_TIMEOUT']
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

auth = HTTPBasicAuth()

from sherlockapi.data import model
from sherlockapi.helpers.util import project_loader

from sherlockapi.views.users import user
from sherlockapi.views.projects import project
from sherlockapi.views.scenarios import scenario
from sherlockapi.views.dashboard import dashboard
from sherlockapi.views.testcases import test_case
from sherlockapi.views.cycles import cycle


app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(project, url_prefix='/project')
app.register_blueprint(cycle, url_prefix='/projects/<int:project_id>/')
app.register_blueprint(scenario, url_prefix='/scenario')
app.register_blueprint(test_case, url_prefix='/scenarios/<int:scenario_id>/tst_case')


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify(message="ENDPOINT_NOTFOUND"), 404)


@app.before_request
def before_request():
    project_loader(model.Project)


@auth.verify_password
def verify_password(username_or_token, password):
    try:
        if model.User.verify_auth_token(username_or_token):
            g.user = model.User.verify_auth_token(username_or_token)
            return True
        else:
            g.user = model.User.query.filter_by(email=username_or_token).first()
            if g.user and g.user.verify_password(password):
                return True
            else:
                return False
    except:
        return False


@app.route('/auth_token', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(6000)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})
