'''Sherlock User Controllers and Routes.'''
from flask import Blueprint, request, g, jsonify, abort, make_response

from sherlock import db, auth
from sherlock.helpers.string_operations import check_str_none_and_blank
from sherlock.data.model import User, UsersSchema

user = Blueprint('users', __name__)


@user.url_value_preprocessor
def get_user(endpoint, values):
    """Blueprint Object Query."""
    if 'user_id' in values:
        g.user = User.query.filter_by(
            id=values.pop('user_id')).first()
        if not g.user:
            abort(make_response(jsonify(message='USER_NOT_FOUND'), 400))


@auth.login_required
@user.route('/show/<int:user_id>', methods=['GET'])
def show():
    """Return a user."""
    user_schema = UsersSchema(many=False)
    user = user_schema.dump(g.user)
    return make_response(jsonify(user=user))


def check_str_none_and_blank(string, name):
    if string is None:
        abort(make_response(jsonify(message='MISSING_{}'.format(name)), 400))
    if string.strip() == '':
        abort(make_response(jsonify(message='BLANK_{}'.format(name)), 400))

@user.route('/new/', methods=['POST'])
def new():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    check_str_none_and_blank(name)
    check_str_none_and_blank(email)
    check_str_none_and_blank(password)

    if User.query.filter_by(email = email).first() is not None:
        abort(make_response(jsonify(message='EMAIL_IN_USE'), 400))

    new_user = User(name=request.get_json().get('name'),
                    email=request.get_json().get('email'),
                    password=request.get_json().get('password'),
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(status='USER_CREATED'))


@auth.login_required
@user.route('/edit/<int:user_id>', methods=['POST'])
def edit():
    edited_user = g.user

    name = request.get_json().get('name')
    email = request.get_json().get('email')
    password = request.get_json().get('password')

    if name:
        check_str_none_and_blank(name)
        edited_user.name = name

    if email:
        check_str_none_and_blank(email)
        if not User.query.filter_by(username=email).first():
            edited_user.username = email
        else:
            abort(make_response(jsonify(message='EMAIL_IN_USE'), 400))

    if password:
        check_str_none_and_blank(password)
        edited_user.password = g.user.generate_hash_password(password)

    db.session.add(edited_user)
    db.session.commit()
    return make_response(jsonify(status='USER_EDITED'))
