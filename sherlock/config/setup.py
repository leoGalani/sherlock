"""Setup script to create and populate the database."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sherlock.config.database_models import Base, User

engine = create_engine('sqlite:///sherlock/config/sherlock.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

initial_user = User(name="Sherlock", user_name="sherlock")
session.add(initial_user)
session.commit()
