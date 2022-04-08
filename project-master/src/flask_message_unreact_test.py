'''
high level support for functions
'''
import requests
import helper
from echo_http_test import url

def test_message_unreact(url):
    # clear,register a user and create a channel
    result = helper.flask_set_up(url)
    token_1 = result['token']
    channel_id = result['channel_id']
   
    response = requests.post(f"{url}/auth/register", json={
        "email": "test02@gmail.com",
        "password": "111111",
        "name_first":"Alice",
        "name_last": "Green"
    })
    payload = response.json()
    token_2 = payload['token']
    u_id_2 = payload['u_id']
    
    requests.post(f"{url}/channel/invite", json={
        "token": token_1,
        "channel_id": channel_id,
        "u_id": u_id_2
    })

    response = requests.post(f"{url}/message/send", json={
        "token": token_1,
        "channel_id": channel_id,
        "message": "Hi"
    })
    payload = response.json()
    message_id = payload['message_id']

    requests.post(f"{url}/message/react", json={
        "token": token_2,
        "message_id": message_id,
        "react_id": 1
    })

    requests.post(f"{url}/message/react", json={
        "token": token_1,
        "message_id": message_id,
        "react_id": 1
    })

    response = requests.post(f"{url}/message/unreact", json={
        "token": token_1,
        "message_id": message_id,
        "react_id": 1
    })

    #response = requests.get(f"{url}/channel/messages", json={
    #    "token": token_1,
    #    "channel_id": channel_id,
    #    "start":0
    #})
    response = requests.get(f"{url}/channel/messages",params={'token':token_1,'channel_id':channel_id,'start':0})
    payload = response.json()
    assert len(payload['messages'][0]['reacts']) == 1
    assert len(payload['messages'][0]['reacts'][0]['u_ids']) == 1
    assert payload['messages'][0]['reacts'][0]['u_ids'] == [2]
    assert payload['messages'][0]['reacts'][0]['is_this_user_reacted'] == False
    assert payload['messages'][0]['reacts'][0]['react_id'] == 1
    
    requests.post(f"{url}/message/unreact", json={
        "token": token_2,
        "message_id": message_id,
        "react_id": 1
    })

    #response = requests.get(f"{url}/channel/messages", json={
    #    "token": token_1,
    #    "channel_id": channel_id,
    #    "start":0
    #})
    response = requests.get(f"{url}/channel/messages",params={'token':token_1,'channel_id':channel_id,'start':0})
    payload = response.json()
    assert len(payload['messages'][0]['reacts']) == 0 


def test_message_id(url):
    '''if message_id not in channel, raise InputError'''
    # clear,register a user and create a channel
    result = helper.flask_set_up(url)
    token_1 = result['token']

    response = requests.post(f"{url}/message/unreact", json={
        "token": token_1,
        "message_id": 1,
        "react_id": 1
    })
    assert response.status_code == 400

def test_react_id(url):   
    '''if react_id != 1, raise InputError''' 
    # flask_set_up clears, registers a user and creates a channel
    result = helper.flask_set_up(url) 
    token_1 = result['token']
    channel_id = result['channel_id']

    response = requests.post(f"{url}/message/send", json={
        "token": token_1,
        "channel_id": channel_id,
        "message": "Hi"
    })
    payload = response.json()
    message_id = payload['message_id']

    response = requests.post(f"{url}/message/unreact", json={
        "token": token_1,
        "message_id": message_id,
        "react_id": 0
    })
    payload = response.json()
    assert response.status_code == 400
   
def test_no_react(url): 
    '''if no react in message, raise InputError'''
    # flask_set_up clears, registers a user and creates a channel
    result = helper.flask_set_up(url) 
    token_1 = result['token']
    channel_id = result['channel_id']

    response = requests.post(f"{url}/message/send", json={
        "token": token_1,
        "channel_id": channel_id,
        "message": "Hi"
    })
    payload = response.json()
    message_id = payload['message_id']

    response = requests.post(f"{url}/message/unreact", json={
        "token": token_1,
        "message_id": message_id,
        "react_id": 1
    })
    assert response.status_code == 400

def user_reacted(url):
    '''if user reacted before, raise InputError'''
    # flask_set_up clears, registers a user and creates a channel
    result = helper.flask_set_up(url) 
    token_1 = result['token']
    channel_id = result['channel_id']

    response = requests.post(f"{url}/message/send", json={
        "token": token_1,
        "channel_id": channel_id,
        "message": "Hi"
    })
    payload = response.json()
    message_id = payload['message_id']
    
    requests.post(f"{url}/message/react", json={
        "token": token_1,
        "message_id": message_id,
        "react_id": 1
    })

    response = requests.post(f"{url}/message/react", json={
        "token": token_1,
        "message_id": message_id,
        "react_id": 1
    })

    assert response.status_code == 400