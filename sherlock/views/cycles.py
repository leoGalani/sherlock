"""Sherlock Cycles Controllers and Routes."""
from flask import Blueprint, request, url_for, redirect, g, jsonify
from flask_login import login_required

from sherlock import db
from sherlock.data.model import Scenario, Project, Case, Cycle


cycle = Blueprint('cycle', __name__)

@cycle.url_value_preprocessor
@login_required
def get_cycles(endpoint, values):
    """Blueprint Object Query."""
    cycles = Cycle.query.filter_by(project_id=values.pop('project_id')).all()
    if cycles:
        g.cycles = cycles
