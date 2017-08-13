# -*- coding: utf8 -*-
"""Configuration params for sherlock."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

TOKEN_TIMEOUT = 9999
SECRET_KEY = 'something-i-hope-you-will-never-figure-out'
#dburl = 'root:@sherlock-mysql/sherlockdb'
dburl = 'root:@localhost/sherlockdb'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}'.format(dburl)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_RECYCLE = 280
