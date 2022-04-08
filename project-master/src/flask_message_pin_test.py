'''
high level support for functions
'''
import pytest
import requests
import message
from helper import flask_set_up
from echo_http_test import url
from error import InputError, AccessError

def test_message_pin(url):
    '''testing function for message_edit'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    result = flask_set_up(url)
    #send message hi
    response = requests.post(f"{url}/message/send", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": "Hi"
    })
    payload = response.json()
    message_id = payload["message_id"]
    # edit message to hello
    response = requests.post(f"{url}/message/pin", json={
        "token": result["token"],
        "message_id": message_id
    })
    # get messages, start from zero
    response = requests.get(f"{url}/channel/messages", params={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "start":0
    })
    payload = response.json()
    # assert message sent is now "Hello"
    print(payload)
    assert payload['messages'][0]['is_pinned'] is True

def test_message_is_pinned(url):
    '''if new text is an empty string, message deleted'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    result = flask_set_up(url)
    #send message hi
    response = requests.post(f"{url}/message/send", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": "Hi"
    })
    payload = response.json()
    message_id = payload['message_id']
    #edit message to be empty string
    response = requests.post(f"{url}/message/pin", json={
        "token": result["token"],
        "message_id": message_id
    })
    response = requests.post(f"{url}/message/pin", json={
            "token": result["token"],
            "message_id": message_id
        })
    assert response.status_code == 400

def test_invalid_token(url):
    '''testing user authorised or not'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    requests.delete(f"{url}/clear", json={})
    # edit a message that doesn't exist with an invalid token
    response = requests.post(f"{url}/message/pin", json={
            "token": 1,
            "message_id": 3
    })

    assert response.status_code == 400


def test_non_member(url):
    '''if user neither flockr owner nor channel owner, raise AccessError'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    result = flask_set_up(url)
    # register a new user
    response = requests.post(f"{url}/auth/register", json={
        "email": "test02@gmail.com",
        "password": "111111",
        "name_first":"John",
        "name_last": "Smith"
        })
    payload = response.json()
    token = payload['token']
    response = requests.post(f"{url}/message/send", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": "Hi"
    })
    payload = response.json()
    message_id = payload['message_id']
    # try and edit a message when user is not flockr/channel owner
    response = requests.post(f"{url}/message/pin", json={
            "token": token,
            "message_id": message_id
    })
    assert response.status_code == 400

def test_invalid_message(url):
    '''if user neither flockr owner nor channel owner, raise AccessError'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    result = flask_set_up(url)
    response = requests.post(f"{url}/auth/register", json={
        "email": "test02@gmail.com",
        "password": "111111",
        "name_first":"John",
        "name_last": "Smith"
        })
    payload = response.json()
    token = payload['token']
    response = requests.post(f"{url}/message/send", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": "Hi"
    })
    payload = response.json()
    message_id = payload['message_id']
    message_id = 'message_id + 3'
    # try and edit a message when user is not flockr/channel owner
    response = requests.post(f"{url}/message/pin", json={
            "token": token,
            "message_id": message_id
    })
    assert response.status_code == 400
