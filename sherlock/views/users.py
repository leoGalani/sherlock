'''Sherlock User Controllers and Routes.'''
from flask import Blueprint, request, g, jsonify, abort, make_response

from sherlock import db, auth
from sherlock.data.model import User, UsersSchema

user = Blueprint('users', __name__)


@user.url_value_preprocessor
def get_user(endpoint, values):
    '''Blueprint Object Query.'''
    if 'user_id' in values:
        g.user = User.query.filter_by(
            id=values.pop('user_id')).first()
        if not g.user:
            return jsonify({'status': 'nok',
                            'msg': 'USER_NOT_FOUND'})


@auth.login_required
@user.route('/show/<int:user_id>', methods=['GET'])
def show():
    '''Return a user.'''
    user_schema = UsersSchema(many=False)
    user = user_schema.dump(g.user)
    return jsonify({'status': 'ok', 'user': user})


@user.route('/new/', methods=['POST'])
def new():
    email = request.json.get('email')
    password = request.json.get('password')

    if email is None:
        abort(make_response(jsonify(message="MISSING_EMAIL"), 400))
    if password is None:
        abort(make_response(jsonify(message="MISSING_PASSWORD"), 400))
    if User.query.filter_by(email = email).first() is not None:
        abort(make_response(jsonify(message="EMAIL_IN_USE"), 400))

    new_user = User(name=request.get_json().get('name'),
                    email=request.get_json().get('email'),
                    password=request.get_json().get('password'),
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(status="USER_CREATED"))


@auth.login_required
@user.route('/edit/<int:user_id>', methods=['POST'])
def edit():
    edited_user = g.user
    if request.get_json().get('name'):
        edited_user.name = request.get_json().get('name')

    if request.get_json().get('email'):
        user = User.query.filter_by(username=email).one_or_none()
        if not user:
            edited_user.username = request.get_json().get('email')
        else:
            abort(make_response(jsonify(message="EMAIL_IN_USE"), 400))

    if request.get_json().get('password'):
        edited_user.password = g.user.generate_hash_password(
            request.get_json().get('password')
        )

    db.session.add(edited_user)
    db.session.commit()
    return make_response(jsonify(status="USER_EDITED"))
