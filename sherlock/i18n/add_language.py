#!flask/bin/python
"""Script that update and add new language support.

To run this script you need to specify the language you are trying to add

Exemple of use:
    python add_language.py pt_br

The language code must be the same as on the config.py file located
on root folder.
"""
import os
import sys

pybabel = 'pybabel'

e = '{} extract -F ../babel.cfg -k lazy_gettext -o messages.pot ../'.format(
    pybabel)
os.system(e)
init = '{} init -i messages.pot -d translations -l {}'.format(
    pybabel, sys.argv[1])
os.system(init)
os.unlink('messages.pot')
