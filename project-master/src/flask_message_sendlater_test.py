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
    response = requests.post(f"{url}/message/sendlater", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": "Hi",
        "time_sent": 9999999999
    })
    payload = response.json()
    #print(payload)
    assert payload['message_id'] == 1

def test_message_length(url):
    '''if message length > 1000, raise InputError'''
    # flask_set_up clears, and registers a user
    # and creates a channel
    result = helper.flask_set_up(url)
    string = ''
    for i in range(1001):
        string = string + str(i)
    response = requests.post(f"{url}/message/sendlater", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": string,
        "time_sent": 9999999999
        })
    # assert response is bad request, 400
    assert response.status_code == 400

def test_sender_membership(url):
    '''if sender not member of channel, raise AccessError'''
    # request to clear and register a user
    requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : "test01@gmail.com",
        "password": "111111",
        "name_first":"John",
        "name_last": "Smith"
        })
    payload = response.json()
    token = payload['token']
    # send a message where sender is not member of a channel
    response = requests.post(f"{url}/message/sendlater", json={
        "token": token,
        "channel_id": 1,
        "message": "Hi",
        "time_sent": 9999999999
    })
    payload = response.json()
    # assert response is AccessError, 500
    assert response.status_code == 400

def test_time_past(url):
    '''if time sent is  in the past, raise InputError'''
     # flask_set_up clears, and registers a user
    # and creates a channel
    result = helper.flask_set_up(url)
    response = requests.post(f"{url}/message/sendlater", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": "Hi",
        "time_sent": 0000000000
    })
    # assert response is bad request, 400
    assert response.status_code == 400
