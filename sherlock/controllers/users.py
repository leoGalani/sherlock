"""Sherlock User Controllers and Routes."""

from flask import Blueprint

from sherlock.config.database_models import User
from sherlock.db import connect


user = Blueprint('users_controller', __name__)
session = connect()


@user.route('/')
@user.route('/<int:user_id>')
def show(user_id):
    """Docstring."""
    user = session.query(User).filter_by(id=user_id).one()
    return user.name
