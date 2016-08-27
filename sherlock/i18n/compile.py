#!flask/bin/python
"""Compile i18n files.
To run this pybabel compiler, you must be on the current directory
"""

import os

os.system('pybabel compile -d translations')
