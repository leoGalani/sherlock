"""Commom string operations."""
import re
from unidecode import unidecode

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Return slug item."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return str(delim.join(result))


def is_empty(obj):
    return len(obj) == 0


def check_str_none_and_blank(string, name):
    if string is None:
        abort(make_response(jsonify(message='MISSING_{}'.format(name)), 400))
    if string.strip() == '':
        abort(make_response(jsonify(message='BLANK_{}'.format(name)), 400))
