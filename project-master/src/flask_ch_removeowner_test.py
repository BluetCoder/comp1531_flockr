'''
high level support for functions
'''
import requests
from echo_http_test import url

def test_empty_input(url):
    """ Test empty input """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/channel/removeowner", json={
        'token': '',
        'channel_id': None,
        'u_id': None
    })
    assert response.status_code == 400

def test_wrong_channel(url):
    """ Test wrong channel """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload1 = response.json()
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test02@gmail.com',
        'password': '2222222',
        'name_first':'Alice',
        'name_last': 'Green'
        })
    register_payload2 = response.json()
    response = requests.post(f"{url}/channel/removeowner", json={
        'token': register_payload1['token'],
        'channel_id': '69',
        'u_id': register_payload2['u_id']
    })
    assert response.status_code == 400

def test_not_owner(url):
    """ Test when user is not owner """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload1 = response.json()
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test02@gmail.com',
        'password': '2222222',
        'name_first':'Alice',
        'name_last': 'Green'
        })
    register_payload2 = response.json()
    response = requests.post(f"{url}/channels/create", json={
        'token': register_payload1['token'],
        'name': "James' Channel",
        'is_public': True
        })
    channels_payload = response.json()
    response = requests.post(f"{url}/channel/join", json={
        'token': register_payload2['token'],
        'channel_id': channels_payload['channel_id']
    })
    response = requests.post(f"{url}/channel/removeowner", json={
        'token': register_payload2['token'],
        'channel_id': channels_payload['channel_id'],
        'u_id': register_payload1['u_id']
    })
    
    assert response.status_code == 400
