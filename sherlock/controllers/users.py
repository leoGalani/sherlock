"""Sherlock User Controllers and Routes."""
from flask import Blueprint, request, url_for, redirect, g

from sherlock import db
from sherlock.data.model import User

user = Blueprint('users', __name__)


@user.url_value_preprocessor
def get_user(endpoint, values):
    """Blueprint Object Query."""
    if 'user_id' in values:
        g.user = User.query.filter_by(
            id=values.pop('user_id')).first_or_404()


@user.route('/show/<int:user_id>', methods=['GET'])
def show():
    """Return a user."""
    return "{} e o nome de usuário é {} com a senha {}".format(
        g.user.name, g.user.username, g.user.password
    )


@user.route('/new/', methods=['GET', 'POST'])
def new():
    """POST endpoint for new users.

    Param:
        name(required)
        user_name(required).
    """
    if request.method == 'POST':
        new_user = User(name=request.form['name'],
                        user_name=request.form['username'],
                        password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users.show', user_id=new_user.id))
    elif request.method == 'GET':
        pass
        # TODO render template of the form.


@user.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit():
    """POST endpoint for editing existing users.

    Param:
        user_id
        user_name
        name
        password
    """
    if request.method == 'POST':
        edited_user = g.user
        edited_user.name = request.form['name']
        edited_user.username = request.form['username']
        edited_user.password = request.form['password']
        db.session.add(edited_user)
        db.session.commit()
        return redirect(url_for('users.show', user_id=g.user.id))
    elif request.method == 'GET':
            pass
            # TODO render template of the form.
