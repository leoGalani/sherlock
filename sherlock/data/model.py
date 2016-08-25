"""Setup for SHERLOCK database."""
import bcrypt
from marshmallow import Schema, fields
from datetime import datetime

from sherlock import db
from sherlock.helpers.string_operations import slugify


class State(db.Model):
    """Static State Table to avoid Enum."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    code = db.Column(db.String(20), unique=True)

    def __init__(self, name, code):
        """Setting params to the object."""
        self.name = name
        self.code = code

    def __repr__(self):
        """Representative Object Return."""
        return '<State %r>' % self.name


class Project(db.Model):
    """Project Schema."""

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)

    scenario = db.relationship('Scenario')

    def __init__(self, name):
        """Setting params to the object."""
        self.name = name
        self.slug = slugify(name)

    def __repr__(self):
        """Representative Object Return."""
        return '<Project %r>' % self.name


class Scenario(db.Model):
    """Scenario` Schema."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    state_code = db.Column(db.Integer, db.ForeignKey('state.code'),
                         default="ACTIVE")
    state = db.relationship('State')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    testcase = db.relationship('Case')

    def __init__(self, name, project_id):
        """Setting params to the object."""
        self.name = name
        self.project_id = project_id

    def __repr__(self):
        """Representative Object Return."""
        return '<Scenario %r>' % self.name


class Case(db.Model):
    """TestCase Schema."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    state_code = db.Column(db.Integer, db.ForeignKey('state.code'),
                         default="ACTIVE")
    state = db.relationship('State')

    def __init__(self, name, scenario_id):
        """Setting params to the object."""
        self.name = name
        self.scenario_id = scenario_id

    def __repr__(self):
        """Representative Object Return."""
        return '<Test_Case %r>' % self.name


class User(db.Model):
    """User Schema."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, name, username, password):
        """Setting params to the object."""
        self.name = name
        self.username = username
        self.password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        """Representative Object Return."""
        return '<User %r>' % self.username


class Cycle(db.Model):
    """Cycle Schema."""

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(500), nullable=False)
    project = db.relationship('Project')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    state = db.relationship('State')
    state_code = db.Column(db.Integer, db.ForeignKey('state.code'),
                         default="ACTIVE")
    cycle_history = db.relationship('CycleHistory')
    created_at = db.Column(db.DateTime, default=datetime.now)
    closed_at = db.Column(db.DateTime)

    def __init__(self, number, project_id):
        """Setting params to the object."""
        self. number = number
        self.project_id = project_id

    def __repr__(self):
        """Representative Object Return."""
        return '<Cycle %r>' % self.id


class CycleHistory(db.Model):
    """Cycle History Schema."""

    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    state_code = db.Column(db.Integer, db.ForeignKey('state.code'),
                         default="NOT_EXECUTED")
    state = db.relationship('State')
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))

    def __init__(self, cycle_id, scenario_id, case_id):
        """Setting params to the object."""
        self.cycle_id = cycle_id
        self.case_id = case_id
        self.scenario_id = scenario_id

    def __repr__(self):
        """Representative Object Return."""
        return '<Cycle %r>' % self.cycle_id


#  SCHEMAS #####

class TestCaseSchema(Schema):
    id = fields.Int(dump_only=True)
    scenario_id = fields.Int()
    name = fields.Str()
    state_code = fields.Int()
