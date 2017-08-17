"""Sherlock User Controllers and Routes."""
from flask import Blueprint, request, jsonify, make_response, abort, g

from sherlockapi import db, auth
from sherlockapi.helpers.string_operations import check_none_and_blank
from sherlockapi.helpers.util import get_user
from sherlockapi.data.model import User, UsersSchema, SherlockSettings

user = Blueprint('users', __name__)


@user.route('/get_all_users', methods=['GET'])
@auth.login_required
def get_all_users():
    user_schema = UsersSchema(many=True)
    users = user_schema.dump(User.query.all()).data
    return make_response(jsonify(users))


@user.route('/get_user_id/<int:user_id>', methods=['GET'])
@auth.login_required
def show_user_id(user_id):
    """Return a user.
    {
        "email": "email@email.com",
        "id": 1,
        "name": "Name"
    }
    """
    user = get_user({'id': user_id})
    user_schema = UsersSchema(many=False)
    user = user_schema.dump(user).data
    return make_response(jsonify(user))


@user.route('/get_user_email/<email>', methods=['GET'])
@auth.login_required
def show_user_email(email):
    """Return a user.
    {
        "email": "email@email.com",
        "id": 1,
        "name": "Name"
    }
    """
    user = get_user({'email': email})
    user_schema = UsersSchema(many=False)
    user = user_schema.dump(user).data
    return make_response(jsonify(user))


@user.route('/new', methods=['POST'])
def new():
    """
    Param:
    {
        'name': required,
        'email': required,
        'password': required
     }
    """
    open_user_setting = SherlockSettings.query.filter_by(
        setting='OPEN_USER_REGISTER').first()

    try:
        if g.user.profile == 'admin':
            is_admin = True
        else:
            is_admin = False
    except:
        is_admin = False

    if open_user_setting == "False" and not is_admin:
        return make_response(jsonify(message='UNAUTHORIZED'))

    name = check_none_and_blank(request, 'name')
    email = check_none_and_blank(request, 'email')
    password = check_none_and_blank(request, 'password')

    if User.query.filter_by(email=email).first() is not None:
        return make_response(jsonify(message='EMAIL_IN_USE'))

    new_user = User(name=name,
                    email=email,
                    password=password)
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(message='USER_CREATED'))


@user.route('/edit/<int:user_id>', methods=['POST'])
@auth.login_required
def edit(user_id):
    """
    Param:
    {
        'name': not_required,
         'email': not_required,
         'password': not_required
    }
    """
    if g.user.id != user_id:
        return make_response(jsonify(message='NOT_ALLOWED'))

    edited_user = g.user

    if 'name' in request.json:
        edited_user.name = check_none_and_blank(request, 'name')

    if 'email' in request.json:
        email = check_none_and_blank(request, 'email')
        if not User.query.filter_by(email=email).first():
            edited_user.email = email

    if 'password' in request.json:
        pwd_raw = check_none_and_blank(request, 'password')
        password = edited_user.generate_hash_password(pwd_raw)
        edited_user.password = password

    db.session.add(edited_user)
    db.session.commit()
    return make_response(jsonify(message='USER_EDITED'))
