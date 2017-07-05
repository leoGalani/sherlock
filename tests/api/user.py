import pytest
import requests
import json

from flask import url_for

from helper import user_hash

@pytest.fixture
def user(client):
    payload = {
        'name': 'test user',
        'email': 'test1@user.xpto',
        'password': 'password'
    }
    header = {'Content-Type': 'application/json'}

    response = client.post(url_for('users.new'),
                           data=json.dumps(payload),
                           headers=header)

    assert response.json['message'] == 'USER_CREATED'
    return payload

@pytest.mark.first
def test_login(client, user):
    header = {'Authorization': user_hash(user['email'], user['password']),
              'Content-Type': 'application/json'}
    response = client.open(url_for('get_auth_token'), method='POST', headers=header)
    assert 'token' in response.json


@pytest.mark.seccond
def test_new_user_email_already_in_use(client, user):
    payload = {
        'name': 'test user',
        'email': user['email'],
        'password': user['password']
    }
    header = {'Content-Type': 'application/json'}

    response = client.post(url_for('users.new'),
                           data=json.dumps(payload),
                           headers=header)

    assert response.json['message'] == 'EMAIL_IN_USE'


#@pytest.mark.second
#def test_show_user():

#@pytest.mark.first
#def test_show_user(login):
