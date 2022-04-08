'''
high level support for functions
'''
import requests
from helper import flask_set_up
from echo_http_test import url

def test_message_edit(url):
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
    response = requests.put(f"{url}/message/edit", json={
        "token": result["token"],
        "message_id": message_id,
        "message": "Hello"
    })
    # get messages, start from zero
    #response = requests.get(f"{url}/channel/messages", json={
    #    "token": result["token"],
    #    "channel_id": result["channel_id"],
    #    "start":0
    #})
    response = requests.get(f"{url}/channel/messages",params={'token':result['token'],'channel_id':result['channel_id'],'start':0})
    payload = response.json()
    # assert message sent is now "Hello"
    assert payload['messages'][0]['message'] == 'Hello'

def test_empty_input(url):
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
    response = requests.put(f"{url}/message/edit", json={
        "token": result["token"],
        "message_id": message_id,
        "message": ""
    })
    payload = response.json()
    #assert message is now ""
    assert payload == {}

def test_invalid_token(url):
    '''testing user authorised or not'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    requests.delete(f"{url}/clear", json={})
    # edit a message that doesn't exist with an invalid token
    response = requests.put(f"{url}/message/edit", json={
        "token": "test01@gmail.com",
        "message_id":1,
        "message": "ta"
    })
    # assert bad response, 400
    assert response.status_code == 400

def test_non_owner(url):
    '''if user neither flockr owner nor channel owner, raise AccessError'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    flask_set_up(url)
    # register a new user
    response = requests.post(f"{url}/auth/register", json={
        "email": "test02@gmail.com",
        "password": "111111",
        "name_first":"John",
        "name_last": "Smith"
        })
    payload = response.json()
    token = payload['token']
    # try and edit a message when user is not flockr/channel owner
    response = requests.put(f"{url}/message/edit", json={
        "token": token,
        "message_id":1,
        "message": "ta"
    })
    assert response.status_code == 400
