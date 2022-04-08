''' high level support functions '''
import requests
from echo_http_test import url

def test_valid(url):
    '''testing function for channels_create'''
    # requests to clear and register a user
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()

    token = payload['token']
    u_id = payload['u_id']
    assert u_id == 1
    # create a channel
    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "coding",
        "is_public": True
    })

    payload = response.json()
    # assert channel_id == 1
    channel_id = payload['channel_id']
    assert channel_id == 1

def test_invalid_channel_name(url):
    '''testing function for channels_create, invalid name'''
    # requests to clear and register a user
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()

    token = payload['token']
    u_id = payload['u_id']
    assert u_id == 1

    # create a channel with an invalid name
    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "thisisdefinitelymorethantwentycharacters",
        "is_public": "True"
    })
    # assert bad request, error 400
    payload = response.json()
    assert payload['code'] == 400

def test_invalid_token(url):
    '''testing function for channels_create, invalid token'''
    # request to clear and create channel with an invalid token
    response = requests.delete(f"{url}/clear", json={})

    token = "thisisnotatoken"
    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "disguised toast",
        "is_public": "True"
    })

    payload = response.json()
    # assert 400 error
    assert payload['code'] == 400
