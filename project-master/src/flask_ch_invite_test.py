'''
high level support for functions
'''
import requests
from echo_http_test import url

def test_invite(url):
    ''' valid invite'''
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
    response = requests.post(f"{url}/channel/invite", json={
        'token': register_payload1['token'],
        'channel_id': channels_payload['channel_id'],
        'u_id': register_payload2['u_id']
    })
    response = requests.get(f"{url}/channel/details", params={
        'token': register_payload1['token'],
        'channel_id': channels_payload['channel_id']
    })
    details_payload = response.json()
    print(details_payload)

    assert details_payload['all_members'] == [
        {
            'u_id': 1,
            'name_first' : 'James',
            'name_last' : 'Turner'
        },
        {
            'u_id': 2,
            'name_first' : 'Alice',
            'name_last' : 'Green'
        }
    ]

def test_invalid_channel(url):
    '''test invalid channel as input of channel_invite function'''

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
    response = requests.post(f"{url}/channel/invite", json={
        'token': register_payload1['token'],
        'channel_id': 69,
        'u_id': register_payload2['u_id']
    })
    assert response.status_code == 400

def test_invalid_user(url):
    '''test invalid user as input of channel_invite function'''

    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload1 = response.json()
    response = requests.post(f"{url}/channels/create", json={
        'token': register_payload1['token'],
        'name': "James' Channel",
        'is_public': True
        })
    channels_payload = response.json()
    response = requests.post(f"{url}/channel/invite", json={
        'token': register_payload1['token'],
        'channel_id': channels_payload['channel_id'],
        'u_id': 69
    })
    assert response.status_code == 400
