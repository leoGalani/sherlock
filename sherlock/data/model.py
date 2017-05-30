"""Setup for SHERLOCK database."""
from datetime import datetime

import bcrypt
from marshmallow import Schema, fields
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from sherlock import db, secretkey
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


class Project(db.Model):
    """Project Schema."""

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_of_project = db.Column(db.String(50), nullable=False)
    is_private = db.Column(db.Boolean, nullable=False)

    scenario = db.relationship('Scenario')

    def __init__(self, name, owner, type_of_project, is_private):
        """Setting params to the object."""
        self.name = name
        self.slug = slugify(name)
        self.owner = owner
        self.type_of_project = type_of_project
        self.is_private = is_private


    def __repr__(self):
        """Representative Object Return."""
        return '<Project %r>' % self.name


class Tags(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))


    def __init__(self, name, scenario_id):
        """Setting params to the object."""
        self.name = name
        self.scenario_id = scenario_id


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
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, password):
        """Setting params to the object."""
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password):
        password = pwd.encode('utf-8')
        if bcrypt.hashpw(password, self.password) == self.password:
            return True
        return False

    @staticmethod
    def generate_hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def generate_auth_token(self, expiration=600):
        s = Serializer(secretkey, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secretkey)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


class Cycle(db.Model):
    """Cycle Schema."""

    id = db.Column(db.Integer, primary_key=True)
    cycle = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Stringer(250))
    project = db.relationship('Project')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    state = db.relationship('State')
    state_code = db.Column(db.Integer, db.ForeignKey('state.code'),
                         default="ACTIVE")
    cycle_history = db.relationship('CycleHistory')
    created_at = db.Column(db.DateTime, default=datetime.now)
    closed_at = db.Column(db.DateTime)
    last_change = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, cycle, project_id):
        """Setting params to the object."""
        self.cycle = cycle
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
    notes = db.Column(db.Text())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime)

    def __init__(self, cycle_id, scenario_id, case_id, notes, created_by):
        """Setting params to the object."""
        self.cycle_id = cycle_id
        self.case_id = case_id
        self.scenario_id = scenario_id
        self.notes = notes
        self.created_by = created_by
        self.created_at = datetime.now

    def __repr__(self):
        """Representative Object Return."""
        return '<Cycle %r>' % self.cycle_id


#  SCHEMAS #####

class TestCaseSchema(Schema):
    id = fields.Int(dump_only=True)
    scenario_id = fields.Int()
    name = fields.Str()
    state_code = fields.Int()


class UsersSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str()
