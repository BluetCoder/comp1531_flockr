''' high level support functions '''
import requests
from echo_http_test import url
from helper import flask_set_up

def test_invalid_token(url):
    """ testing standup_start with invalid token """
    result = flask_set_up(url)
    response = requests.post(f"{url}/standup/start", json={
        "token": "abc",
        "channel_id": result['channel_id'],
        "length": 100
    })
    assert response.status_code == 400
def test_invalid_ch_id(url):
    """ testing standup_start with invalid channel_id """
    result = flask_set_up(url)
    response = requests.post(f"{url}/standup/start", json={
        "token": result['token'],
        "channel_id": 2,
        "length": 100
    })
    assert response.status_code == 400

def test_valid_standup_start(url):
    """ testing standup_start with valid inputs """
    result = flask_set_up(url)
    response = requests.post(f"{url}/standup/start", json={
        "token": result['token'],
        "channel_id": result['channel_id'],
        "length": 100
    })
    assert response.status_code == 200

def test_invalid_active_standup(url):
    """ testing standup_start with invalid channel_id """
    result = flask_set_up(url)
    response = requests.post(f"{url}/standup/start", json={
        "token": result['token'],
        "channel_id": result['channel_id'],
        "length": 100
    })
    assert response.status_code == 200
    response = requests.post(f"{url}/standup/start", json={
        "token": result['token'],
        "channel_id": result['channel_id'],
        "length": 100
    })
    assert response.status_code == 400
# Need to check if my testing and function are implemented correctly
