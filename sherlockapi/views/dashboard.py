"""Sherlock User Controllers and Routes."""
from flask import Blueprint, g, render_template

from sherlockapi import db, auth
from sherlockapi.data.model import Cycle, CycleHistory
from sherlockapi.helpers.util import load_last_cyle_status_of_projects

dashboard = Blueprint('dashboard', __name__)

#@dashboard.route('/', methods=['GET'])
#@auth.login_required
#def home():
#    if g.projects:
#        g.last_project_cycles = load_last_cyle_status_of_projects(
#            Cycle, CycleHistory, g.projects)
#    return render_template("dashboard.html")
