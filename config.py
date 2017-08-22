# -*- coding: utf8 -*-
"""Configuration params for sherlock."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))
CORS_HEADER = 'Content-Type'
TOKEN_TIMEOUT = 9999
SECRET_KEY = os.urandom(25)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
