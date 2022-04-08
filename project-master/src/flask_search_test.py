'''
high level support for functions
'''
import requests
from echo_http_test import url
from helper import flask_set_up

def test_valid_messages(url):
    ''' search returns valid collection of messages'''
    result = flask_set_up(url)
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'z5309388@unsw.edu.au',
        'password': 'password1',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload2 = response.json()

    response = requests.post(f"{url}/channel/join", json={
        "token" : register_payload2['token'],
        'channel_id': result['channel_id']
        })

    response = requests.post(f"{url}/message/send", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "message": 'message 1'
    })

    response = requests.post(f"{url}/message/send", json={
        "token": register_payload2["token"],
        "channel_id": result["channel_id"],
        "message": 'message 2'
    })

    response = requests.post(f"{url}/message/send", json={
        "token": register_payload2["token"],
        "channel_id": result["channel_id"],
        "message": 'massage 3'
    })

    response = requests.post(f"{url}/message/send", json={
        "token": register_payload2["token"],
        "channel_id": result["channel_id"],
        "message": 'message 4'
    })

    response = requests.post(f"{url}/message/send", json={
        "token": register_payload2["token"],
        "channel_id": result["channel_id"],
        "message": 'massage 6'
    })

    response = requests.post(f"{url}/message/send", json={
        "token": register_payload2["token"],
        "channel_id": result["channel_id"],
        "message": 'massage 9'
    })

    response = requests.get(f"{url}/search",params={'token':result['token'],'query_str':'massage'})
    search_payload = response.json()
    assert search_payload['messages'][0]['message_id'] == 6
    assert search_payload['messages'][1]['message_id'] == 5
    assert search_payload['messages'][2]['message_id'] == 3

def test_empty_messages(url):
    ''' messages removed, Access error raised '''
    result = flask_set_up(url)
    response = requests.get(f"{url}/search",params={'token':result['token'],'query_str':result['channel_id']})
    search_payload = response.json()
    assert search_payload['messages'] == []

def test_user_left_channel(url):
    ''' user no longer part of that channel, no longer returns from that channel '''
    result = flask_set_up(url)
    response = requests.post(f"{url}/channel/leave", json={
        "token": result["token"],
        "channel_id": result['channel_id']
    })
    response = requests.get(f"{url}/search", json={
        "token": result["token"],
        "query_str": 'message'
    })
    assert response.status_code == 400
