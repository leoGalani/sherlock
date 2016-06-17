"""Setup for SHERLOCK database."""
import bcrypt
from marshmallow import Schema, fields


from sherlock import db
from sherlock.helpers.string_operations import slugify


class State(db.Model):
    """Static State Table to avoid Enum."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        """Setting params to the object."""
        self.name = name

    def __repr__(self):
        """Representative Object Return."""
        return '<State %r>' % self.name


class Project(db.Model):
    """Project Schema."""

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)

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

    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    state = db.relationship('State')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, name, state_id, project_id):
        """Setting params to the object."""
        self.name = name
        self.state_id = state_id
        self.project_id = project_id

    def __repr__(self):
        """Representative Object Return."""
        return '<Scenario %r>' % self.name


class Test_Case(db.Model):
    """TestCase Schema."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    scenario = db.relationship(Scenario)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    state = db.relationship('State')

    def __init__(self, name, scenario_id, state_id):
        """Setting params to the object."""
        self.name = name
        self.scenario_id = scenario_id
        self.state_id = state_id

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


#  SCHEMAS #####

class TestCaseSchema(Schema):
    id = fields.Int(dump_only=True)
    scenario_id = fields.Int()
    name = fields.Str()
    state_id = fields.Int()
