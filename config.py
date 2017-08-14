# -*- coding: utf8 -*-
"""Configuration params for sherlock."""
import os
from dbconfig import prod_db

basedir = os.path.abspath(os.path.dirname(__file__))
CORS_HEADER = 'Content-Type'
TOKEN_TIMEOUT = 9999
SECRET_KEY = os.urandom(25)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}'.format(prod_db)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_RECYCLE = 280
