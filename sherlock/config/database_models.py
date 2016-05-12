"""Setup for SHERLOCK database."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Project(Base):
    """Project Schema."""

    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Scenario(Base):
    """Scenario` Schema."""

    __tablename__ = 'scenario'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship(Project)


class TestCase(Base):
    """TestCase Schema."""

    __tablename__ = "test_case"

    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    scenario_id = Column(Integer, ForeignKey('scenario.id'))
    scenario = relationship(Scenario)


class User(Base):
    """User Schema."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_name = Column(String(50), nullable=False)


engine = create_engine('sqlite:///sherlock/config/sherlock.db')
Base.metadata.create_all(engine)
