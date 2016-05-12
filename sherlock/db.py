"""DataBase handler."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sherlock.config.database_models import Base


def connect():
    """Connect Flask with the database."""
    engine = create_engine('sqlite:///sherlock/config/sherlock.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    return DBSession()
