''' high level support functions '''
import requests
from echo_http_test import url
from helper import flask_set_up
import json

def test_invalid_token(url):
    """ testing standup_active with invalid token """
    result = flask_set_up(url)
    response = requests.get(f"{url}/standup/active", params={
        'token': 'abc',
        'channel_id': result['channel_id'],
    })
    assert response.status_code == 400

def test_invalid_ch_id(url):
    """ testing standup_active with invalid channel_id """
    result = flask_set_up(url)
    response = requests.get(f"{url}/standup/active", params={
        "token": result['token'],
        "channel_id": 2,
    })
    assert response.status_code == 400

def test_valid_standup_active(url):
    """ testing standup_active with active standup """
    result = flask_set_up(url)
    # Setting up standup
    response = requests.post(f"{url}/standup/start", json={
        "token": result['token'],
        "channel_id": result['channel_id'],
        "length": 100
    })
    start_payload = response.json()
    response = requests.get(f"{url}/standup/active", params={
        "token": result['token'],
        "channel_id": result['channel_id'],
    })
    active_payload = response.json()
    assert start_payload['time_finish'] == active_payload['time_finish']
    assert active_payload['is_active'] == True

def test_valid_no_active(url):
    """ testing standup_active with no active standup """
    result = flask_set_up(url)

    # Setting up standup
    response = requests.get(f"{url}/standup/active", params={
        "token": result['token'],
        "channel_id": result['channel_id'],
    })
    active_payload = response.json()
    assert active_payload['time_finish'] == None
    assert active_payload['is_active'] == False
