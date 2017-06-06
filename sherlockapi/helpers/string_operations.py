"""Commom string operations."""
import re
from unidecode import unidecode
from flask import abort, make_response, jsonify

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Return slug item."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return str(delim.join(result))


def is_empty(obj):
    return len(obj) == 0


def check_none_and_blank(obj, name):
    name = name.upper()
    if obj is None:
        abort(make_response(jsonify(message='MISSING_{}'.format(name)), 400))

    if type(obj) is str:
        if obj.strip() == '':
            abort(make_response(jsonify(message='BLANK_{}'.format(name)), 400))
    elif type(obj) is list:
        if len(obj) == 0:
            abort(make_response(jsonify(message='EMPTY_{}_LIST'.format(name)), 400))
