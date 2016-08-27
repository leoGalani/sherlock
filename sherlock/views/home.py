"""Sherlock User Controllers and Routes."""
from flask import Blueprint, redirect, url_for

home = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
def home():
    return redirect(url_for('users.login'))
