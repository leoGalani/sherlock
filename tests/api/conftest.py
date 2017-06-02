import pytest
import sys
import os

sys.path.append("../../") #Need to fix it
from sherlock import app as sherlock
from sherlock import app as sherlock

@pytest.fixture(scope='session')
def app():
    return sherlock

@pytest.yield_fixture
def client(app):
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.remove(os.path.join(current_dir, '../../sherlock/data/sherlock.db'))
        os.system('python ../../setup.py')
    except OSError:
        pass
    with app.test_client() as client:
        yield client
