"""Flask and plugin init"""
import os

from flask import Flask, jsonify, make_response, g
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from dbconfig import prod_db
from sherlockapi.blueprints import register_bprints


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

if 'SHERLOCK_ENV' in os.environ:
    if os.environ['SHERLOCK_ENV'] == 'PROD':
        dburl = prod_db()
else:
    from flask_cors import CORS
    CORS(app, resources={r'/*': {"origins": '*', 'allow_headers': '*'}})
    dburl = 'root:@localhost/sherlockdb'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}'.format(dburl)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)
auth = HTTPBasicAuth()
secretkey = app.config['SECRET_KEY']
token_timeout = app.config['TOKEN_TIMEOUT']

# Will load the Models and create the tables
from sherlockapi.data import model

register_bprints(app)


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify(message="ENDPOINT_NOTFOUND"), 404)


@auth.verify_password
def verify_password(username_or_token, password):
    """
    TODO: ajust except.
    """
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


@app.route('/api/auth_token', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(604800)
    return jsonify({'token': token.decode('ascii'), 'duration': 604800})
