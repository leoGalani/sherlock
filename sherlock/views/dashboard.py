"""Sherlock User Controllers and Routes."""
from flask import Blueprint, request, url_for, redirect, g, render_template
from flask import flash
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/', methods=['GET'])
@login_required
def home():
    """Return a user."""
    return render_template("dashboard.html")
