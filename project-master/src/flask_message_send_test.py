'''
high level support for functions
'''
import requests
import helper
from echo_http_test import url

def test_message_send(url):
    '''testing function for message_send'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    result = helper.flask_set_up(url)
    response = requests.post(f"{url}/message/send", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": "Hi"
    })
    response = requests.get(f"{url}/channel/messages",params={'token':result['token'],'channel_id':result['channel_id'],'start':0})
    payload = response.json()
    assert payload['messages'][0]['message_id'] == 1

def test_message_length(url):
    '''if message length > 1000, raise InputError'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    result = helper.flask_set_up(url)
    string = ''
    for i in range(1001):
        string = string + str(i)
    response = requests.post(f"{url}/message/send", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": string
    })
    # assert response is bad request, 400
    assert response.status_code == 400

def test_sender_membership(url):
    '''if sender not member of channel, raise AccessError'''
    # request to clear and register a user
    # requests.delete(f"{url}/clear", json={})
    result = helper.flask_set_up(url)
    response = requests.post(f"{url}/auth/register", json={
        "email" : "test03@gmail.com",
        "password": "111111",
        "name_first":"Harry",
        "name_last": "Potter"
        })
    payload = response.json()
    token = payload['token']
    # send a message where sender is not member of a channel
    response = requests.post(f"{url}/message/send", json={
        "token": token,
        "channel_id": result['channel_id'],
        "message": "Hi"
    })
    # assert response is AccessError, 400
    assert response.status_code == 400
