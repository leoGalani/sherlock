"""Setup for SHERLOCK database."""
from datetime import datetime
from enum import Enum
from flask import g
import bcrypt

from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from sherlockapi import db, secretkey
from sherlockapi.db_init import check_first_run


class StateType(Enum):
    active = "active"
    disable = "disable"
    not_executed = "not_executed"
    passed = "passed"
    error = "error"
    blocked = "blocked"
    ongoing = "ongoing"
    closed = "closed"


class Project(db.Model):
    __tablename__ = "project"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_of_project = db.Column(db.String(50), nullable=False)
    privacy_policy = db.Column(db.String(50), nullable=False)

    scenario = db.relationship('Scenario')
    cycle = db.relationship('Cycle')

    def __init__(self, name, owner_id, type_of_project, privacy_policy):
        """Setting params to the object."""
        self.name = name
        self.owner_id = owner_id
        self.type_of_project = type_of_project
        self.privacy_policy = privacy_policy


    def __repr__(self):
        """Representative Object Return."""
        return '<Project %r>' % self.name


class Scenario(db.Model):
    __tablename__ = "scenario"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    state_code = db.Column(db.Enum(StateType))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    cycle_scenarios = db.relationship('CycleScenarios')
    cycle_cases = db.relationship('CycleCases')
    case = db.relationship('Case')

    def __init__(self, name, project_id):
        self.name = name
        self.project_id = project_id
        self.state_code = StateType.active


class Case(db.Model):
    __tablename__ = "case"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    state_code = db.Column(db.Enum(StateType))

    def __init__(self, name, scenario_id):
        self.name = name
        self.scenario_id = scenario_id
        self.state_code = StateType.active


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    profile = db.Column(db.String(50), nullable=False)

    cycle_scenarios = db.relationship('CycleScenarios')
    project = db.relationship('Project')


    def __init__(self, name, email, password, profile='user'):
        self.name = name
        self.email = email
        self.password = User.generate_hash_password(password)
        self.profile=profile

    def verify_password(self, password):
        password = password.encode('utf-8')
        self.password = self.password.encode('utf-8')
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
        g.user = User.query.get(data['id'])
        return g.user


class Cycle(db.Model):
    __tablename__ = "cycle"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cycle = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(250))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    state_code = db.Column(db.Enum(StateType))

    cycle_cases = db.relationship('CycleCases')
    cycle_scenarios = db.relationship('CycleScenarios')

    created_at = db.Column(db.DateTime, default=datetime.now)
    closed_at = db.Column(db.DateTime)
    closed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    closed_reason = db.Column(db.String(250))
    last_change = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, cycle, name, project_id):
        self.cycle = cycle
        self.name = name
        self.project_id = project_id
        self.state_code = StateType.active


class CycleScenarios(db.Model):
    __tablename__ = "cycle_scenarios"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    state_code = db.Column(db.Enum(StateType))
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    last_executed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_executed_at = db.Column(db.DateTime)

    def __init__(self, cycle_id, scenario_id):
        self.cycle_id = cycle_id
        self.scenario_id = scenario_id
        self.state_code = StateType.not_executed


class CycleCases(db.Model):
    __tablename__ = "cycle_cases"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    state_code = db.Column(db.Enum(StateType))
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    last_executed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_executed_at = db.Column(db.DateTime)

    def __init__(self, cycle_id, scenario_id, case_id):
        """Setting params to the object."""
        self.cycle_id = cycle_id
        self.case_id = case_id
        self.scenario_id = scenario_id
        self.state_code = StateType.not_executed

class ScenarioNotes(db.Model):
    __tablename__ = "notes"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    scenario_id = db.Column(db.Integer)
    text = db.Column(db.String(250))

    def __init__(self, cycle_id, scenario_id,  text):
        """Setting params to the object."""
        self.cycle_id = cycle_id
        self.scenario_id = scenario_id
        self.text = text


class CaseNotes(db.Model):
    __tablename__ = "notes"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    case_id = db.Column(db.Integer)
    text = db.Column(db.String(250))

    def __init__(self, cycle_id, scenario_id,  text):
        self.cycle_id = cycle_id
        self.scenario_id = scenario_id
        self.text = text


class SherlockSettings(db.Model):
    __tablename__ = "sherlock_settings"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    setting = db.Column(db.String(250))
    value = db.Column(db.String(250))
    who_can_change = db.Column(db.String(250))
    label = db.Column(db.String(250))

    def __init__(self, setting, value, label, who_can_change='admin'):
        self.setting = setting
        self.value = value
        self.who_can_change = who_can_change
        self.label = label


#  SCHEMAS #####

class SettingsSchema(Schema):
    id = fields.Int(dump_only=True)
    setting = fields.Str()
    value = fields.Str()
    label = fields.Str()


class CycleSchema(Schema):
    id = fields.Int(dump_only=True)
    cycle = fields.Int()
    project_id = fields.Int()
    name = fields.Str()
    state_code = EnumField(StateType)
    created_at = fields.Str()
    closed_at = fields.Str()
    last_change = fields.Str()


class TestCaseSchema(Schema):
    id = fields.Int(dump_only=True)
    scenario_id = fields.Int()
    name = fields.Str()
    state_code = EnumField(StateType)


class ScenariosSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    state_code = EnumField(StateType)
    project_id = fields.Int()


class UsersSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str()
    profile = fields.Str()


class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    owner_id = fields.Int()
    type_of_project = fields.Str()
    privacy_policy = fields.Str()

check_first_run(db)
