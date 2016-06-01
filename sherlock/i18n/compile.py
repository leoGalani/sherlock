#!flask/bin/python
"""Compile i18n files."""

import os

os.system('pybabel compile -d translations')
