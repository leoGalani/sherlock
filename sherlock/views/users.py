"""Sherlock User Controllers and Routes."""
from flask import Blueprint, request, url_for, redirect, g, render_template
from flask import flash
from flask_login import login_required, login_user
from flask_babel import gettext

import bcrypt

from sherlock import db, login_manager
from sherlock.data.model import User
from sherlock.forms.user import login_form, signup_form, edit_user_form


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
    form = signup_form()
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(username=form.email.data).one_or_none()
        if user:
            flash(gettext('Email already in use'), 'danger')
        else:
            new_user = User(name=request.form['name'],
                            username=request.form['email'],
                            password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('users.login'))

    return render_template("user/signup.html", form=form)


@user.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit():
    form = edit_user_form()
    if request.method == 'POST':
        edited_user = g.user
        edited_user.name = request.form['name']
        edited_user.username = request.form['email']
        edited_user.password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        db.session.add(edited_user)
        db.session.commit()
        return redirect(url_for('dashboard.home'))

    return render_template("user/login.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User.

    param unicode user_id: user_id (username) user to retrieve
    """
    return User.query.filter_by(username=user_id).one_or_none()


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = login_form()

    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(username=form.email.data).one_or_none()
        pwd = form.password.data or ""
        pwd = pwd.encode('utf-8')
        if user and bcrypt.hashpw(pwd, user.password) == user.password:
            login_user(user, remember=True)
            return redirect(url_for("dashboard.home"),)
        else:
            flash(gettext('Wrong credentials'), 'danger')

    return render_template("user/login.html", form=form)
