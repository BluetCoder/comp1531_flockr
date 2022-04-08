'''
high level support for functions
'''
import requests
from echo_http_test import url

def test_empty_input(url):
    """ Test empty input """
    # Clear function
    response = requests.delete(f"{url}/clear", json={})
    # Use empty input to add owner
    response = requests.post(f"{url}/channel/addowner", json={
        'token': '',
        'channel_id': None,
        'u_id': None
    })
    # Should return 400 error
    assert response.status_code == 400

def test_wrong_channel(url):
    """ Test wrong channel """
    # register 2 users, add owner to illegit channel, assert error is raised
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
    response = requests.post(f"{url}/channel/addowner", json={
        'token': register_payload1['token'],
        'channel_id': '69',
        'u_id': register_payload2['u_id']
    })
    assert response.status_code == 400

def test_not_owner(url):
    """ Test when user is not owner """
    # Register 2 users, user1 create channel, user2 join channel, user2 attempt
    # to add user1 as an owner, but user2 not an owner: raise error
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
    response = requests.post(f"{url}/channel/addowner", json={
        'token': register_payload2['token'],
        'channel_id': channels_payload['channel_id'],
        'u_id': register_payload1['u_id']
    })
    assert response.status_code == 400

def test_valid_ch_addowner(url):
    """ Test valid input """
    # register 2 users, create channel u1, join channel u2, add owner u1
    # assert using channel details the owners are both u1 and 2
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
    response = requests.post(f"{url}/channel/addowner", json={
        'token': register_payload1['token'],
        'channel_id': channels_payload['channel_id'],
        'u_id': register_payload2['u_id']
    })
    response = requests.get(f"{url}/channel/details", params={
        'token': register_payload1['token'],
        'channel_id': channels_payload['channel_id']
    })
    #response = requests.get(f"{url}/channel/details",params={
    #    'token':register_payload1['token'],
    #    'channel_id':channels_payload['channel_id']})
    details_payload = response.json()
    assert details_payload['owner_members'] == [
        {
            'u_id': 1,
            'name_first': 'James',
            'name_last': 'Turner'
        },
        {
            'u_id': 2,
            'name_first': 'Alice',
            'name_last': 'Green'
        }
    ]
