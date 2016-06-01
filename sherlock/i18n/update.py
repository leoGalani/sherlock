"""Update translation files for new strings."""
import os

pybabel = 'pybabel'

e = '{} extract -F ../babel.cfg -k lazy_gettext -o messages.pot ../'.format(
    pybabel)
os.system(e)
update = '{} update -i messages.pot -d translations'.format(pybabel)
os.system(update)
os.unlink('messages.pot')
