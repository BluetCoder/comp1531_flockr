'''
high level support for functions
'''
import requests
import helper
from echo_http_test import url

def message_generate(url, length):
    '''generates messages and setup '''
    result = helper.flask_set_up(url)
    i = 0
    while i < length:
        requests.post(f"{url}/message/send", json={
            "token": result["token"],
            "channel_id": result["channel_id"],
            "message": str(i)
        })
        i += 1
    return {"token": result['token'], "channel_id": result['channel_id']}

def test_messages(url):
    '''testing channel_messages function'''
    result = message_generate(url, 100)
    response = requests.get(f"{url}/channel/messages",params={'token':result['token'],'channel_id':result['channel_id'],'start':0})
    payload = response.json()
    assert payload['messages'][0]['message_id'] == 50
    assert payload['messages'][49]['message_id'] == 1
    assert payload['start'] == 0
    assert payload['end'] == 50
    response = requests.get(f"{url}/channel/messages",params={'token':result['token'],'channel_id':result['channel_id'],'start':25})
    payload2 = response.json()
    assert payload2['messages'][0]['message_id'] == 75
    assert payload2['messages'][49]['message_id'] == 26
    assert payload2['start'] == 25
    assert payload2['end'] == 75

def test_invalid_channel(url):
    '''testing invalid channel as input of channel_message function'''
    result = helper.flask_set_up(url)
    response = requests.get(f"{url}/channel/messages", json={
        "token": result["token"],
        "channel_id": 10,
        "start":0
    })
    assert response.status_code == 400

def test_start(url):
    '''testing improper start number'''
    result = message_generate(url, 1)
    response = requests.get(f"{url}/channel/messages", json={
        "token": result["token"],
        "channel_id": result["channel_id"],
        "start":60
    })
    assert response.status_code == 400

def test_member(url):
    '''testing non-member as input of channel_messages function'''
    result = message_generate(url, 1)
    response = requests.post(f"{url}/auth/register", json={
        "email" : "test02@gmail.com",
        "password": "111111",
        "name_first":"John",
        "name_last": "Smith"
        })
    register_payload = response.json()
    response = requests.get(f"{url}/channel/messages", json={
        "token": register_payload["token"],
        "channel_id": result["channel_id"],
        "start": 1
    })
    assert response.status_code == 400

def test_token(url):
    '''testing token validity'''
    result = message_generate(url, 1)
    response = requests.get(f"{url}/channel/messages", json={
        "token": "invalid token",
        "channel_id": result["channel_id"],
        "start": 1
    })
    assert response.status_code == 400

def test_end_value(url):
    '''testing end == -1 when least recent message is returned'''
    result = message_generate(url, 50)
    response = requests.get(f"{url}/channel/messages",params={'token':result['token'],'channel_id':result['channel_id'],'start':0})
    payload = response.json()
    assert payload['start'] == 0
    assert payload['end'] == -1

def test_length_0(url):
    '''test no messages'''
    result = helper.flask_set_up(url)
    response = requests.get(f"{url}/channel/messages",params={'token':result['token'],'channel_id':result['channel_id'],'start':0})
    payload = response.json()
    assert payload == {'end':-1,'messages':[],'start':0}
