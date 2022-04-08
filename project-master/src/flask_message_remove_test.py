'''
high level support for functions
'''
import requests
from echo_http_test import url
from helper import flask_set_up

def test_message_remove(url):
    '''testing function for message_remove'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    result = flask_set_up(url)
    # send message "hi"
    response = requests.post(f"{url}/message/send", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": "Hi"
    })
    payload = response.json()
    message_id = payload['message_id']
    # delete message "hi"
    response = requests.delete(f"{url}/message/remove", json={
        "token": result["token"],
        "message_id": message_id
    })
    # get channel messages
    #response = requests.get(f"{url}/channel/messages", json={
    #    "token": result["token"],
    #    "channel_id": result["channel_id"],
    #    "start":0
    #})
    response = requests.get(f"{url}/channel/messages",params={'token':result['token'],'channel_id':result['channel_id'],'start':0})
    # assert there are no more messages
    payload = response.json()
    #assert payload == {}
    assert payload == {'end':-1,'messages':[],'start':0}

def test_message_nonexistent(url):
    '''testing removing a message which no longer exists'''
    # set up flask
    result = flask_set_up(url)
    # delete a non-existent message
    response = requests.delete(f"{url}/message/remove", json={
        "token": result["token"],
        "message_id": 1
    })
    # assert response is bad request, 400
    assert response.status_code == 400

def test_invalid_token(url):
    '''testing user authorised or not'''
    # request to clear
    requests.delete(f"{url}/clear", json={})
    response = requests.delete(f"{url}/message/remove", json={
        "token": "test01@gmail.com",
        "message_id":1
    })
    # assert response is bad request, 400
    assert response.status_code == 400

def test_non_owner(url):
    '''if user neither flockr owner nor channel owner, raise AccessError'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    flask_set_up(url)
    # register user 2
    response = requests.post(f"{url}/auth/register", json={
        "email": "test02@gmail.com",
        "password": "111111",
        "name_first":"John",
        "name_last": "Smith"
        })
    payload = response.json()
    token = payload['token']
    # request to delete a non-message
    response = requests.delete(f"{url}/message/remove", json={
        "token": token,
        "message_id":1
    })
    payload = response.json()
    # assert response is bad request, 400
    assert response.status_code == 400
