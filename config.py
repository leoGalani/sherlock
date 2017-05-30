# -*- coding: utf8 -*-
"""Configuration params for sherlock."""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

TOKEN_TIMEOUT = 9999
SECRET_KEY = 'something-i-hope-you-will-never-figure-out'

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(
    basedir, 'sherlock/data/sherlock.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = True



# available languages
LANGUAGES = {
    'en_us': 'English',
    'pt_br': 'Portuguese Brasil'
}

BABEL_DEFAULT_LOCALE = 'en_us'
BABEL_DEFAULT_TIMEZONE = 'UTC'
