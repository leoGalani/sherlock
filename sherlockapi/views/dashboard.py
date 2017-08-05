"""Sherlock User Controllers and Routes."""
from flask import Blueprint, request, g, jsonify, make_response, abort

from sherlockapi import db, auth
from sherlockapi.data.model import Cycle, CycleHistory, Project, ProjectSchema
from sherlockapi.helpers.util import load_last_cyle_status_of_projects

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/', methods=['GET'])
@auth.login_required
def home():
    schema = ProjectSchema(many=True)
    projects = schema.dump(Project.query.all()).data

    import random

    for item in projects:
        item['current_cycle'] = 1
        item['cycle_state'] = random.choice(["ACTIVE","CLOSED"])
        item['NOT_EXECUTED'] = 10
        item['PASSED'] = 30
        item['ERROR'] = 10
        item['BLOCKED'] = 1

    return make_response(jsonify(projects=projects))
