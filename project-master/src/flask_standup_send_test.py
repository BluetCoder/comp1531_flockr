''' high level support functions '''
import requests
from echo_http_test import url
from helper import flask_set_up

def test_invalid_token(url):
    """ testing standup_send with invalid token """
    result = flask_set_up(url)
    response = requests.post(f"{url}/standup/send", json={
        "token": "abc",
        "channel_id": result['channel_id'],
        "message": "Hello"
    })
    assert response.status_code == 400

def test_invalid_ch_id(url):
    """ testing standup_send with invalid channel_id """
    result = flask_set_up(url)
    response = requests.post(f"{url}/standup/start", json={
        "token": result['token'],
        "channel_id": result['channel_id'],
        "length": 100
    })
    response = requests.post(f"{url}/standup/send", json={
        "token": result['token'],
        "channel_id": 2,
        "message": "Hello"
    })
    assert response.status_code == 400

def test_invalid_message_length(url):
    '''if message length > 1000, raise InputError'''
    result = flask_set_up(url)

    # Generates a message with over 1000 characters
    string = ''
    for i in range(1001):
        string = string + str(i)
    response = requests.post(f"{url}/standup/start", json={
        "token": result['token'],
        "channel_id": result['channel_id'],
        "length": 100
    })
    response = requests.post(f"{url}/standup/send", json={
        "token": result['token'],
        "channel_id": result['channel_id'],
        "message": string
    })
    assert response.status_code == 400

def test_invalid_no_standup(url):
    """ testing standup_send with no standup """
    result = flask_set_up(url)
    response = requests.post(f"{url}/standup/send", json={
        "token": result['token'],
        "channel_id": result['channel_id'],
        "message": "Hello"
    })
    assert response.status_code == 400

def test_invalid_not_member(url):
    """ testing standup_send with no standup """
    result = flask_set_up(url)

    response = requests.post(f"{url}/standup/start", json={
        "token": result['token'],
        "channel_id": result['channel_id'],
        "length": 100
    })
    response = requests.post(f"{url}/auth/register", json={
        "email" : "test02@gmail.com",
        "password": "111111",
        "name_first":"Harry",
        "name_last": "Potter"
        })
    
    payload = response.json()
    non_member = payload['token']
    response = requests.post(f"{url}/standup/send", json={
        "token": non_member,
        "channel_id": result['channel_id'],
        "message": "Hello"
    })
    assert response.status_code == 400 
# Need to check if my testing and function are implemented correctly
