'''Sherlock User Controllers and Routes.'''
from flask import Blueprint, request, g, jsonify, make_response

from sherlockapi import db, auth
from sherlockapi.helpers.string_operations import check_none_and_blank
from sherlockapi.data.model import User, UsersSchema

user = Blueprint('users', __name__)


@user.url_value_preprocessor
def get_user(endpoint, values):
    """ Blueprint Object Query."""
    if 'user_id' in values:
        g.user = User.query.filter_by(
            id=values.pop('user_id')).first()
        if not g.user:
            return make_response(jsonify(message='USER_NOT_FOUND'), 404)


@user.route('/show/<int:user_id>', methods=['GET'])
@auth.login_required
def show():
    """ Return a user.
        ex:
        {
            "email": "email@email.com",
            "id": 1,
            "name": "Name"
        }
    """
    user_schema = UsersSchema(many=False)
    user = user_schema.dump(g.user).data
    return make_response(jsonify(user))


@user.route('/new/', methods=['POST'])
def new():
    """POST endpoint for new user.

    Param:
        {'name': required,
         'email': required,
         'password': required }
    """
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    check_none_and_blank(name, 'name')
    check_none_and_blank(email, 'email')
    check_none_and_blank(password, 'password')

    if User.query.filter_by(email = email).first() is not None:
        return make_response(jsonify(message='EMAIL_IN_USE'), 400)

    new_user = User(name=request.get_json().get('name'),
                    email=request.get_json().get('email'),
                    password=request.get_json().get('password'))
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(message='USER_CREATED'))


@user.route('/edit/<int:user_id>', methods=['POST'])
@auth.login_required
def edit():
    """POST endpoint for edit user.

    Param:
        {'name': not_required,
         'email': not_required,
         'password': not_required }
    """

    edited_user = g.user
    name = request.get_json().get('name')
    email = request.get_json().get('email')
    password = request.get_json().get('password')

    if name:
        check_none_and_blank(name, 'name')
        edited_user.name = name

    if email:
        check_none_and_blank(email, 'email')
        if not User.query.filter_by(username=email).first():
            edited_user.username = email
        else:
            return make_response(jsonify(message='EMAIL_IN_USE'), 400)

    if password:
        check_none_and_blank(password, 'password')
        edited_user.password = g.user.generate_hash_password(password)

    db.session.add(edited_user)
    db.session.commit()
    return make_response(jsonify(message='USER_EDITED'))
