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
    return True if obj.__len__() == 0 else False


def empty_items_in_dict(dict):
    for item in dict:
        if is_empty(dict[item]):
            return True
    return False
