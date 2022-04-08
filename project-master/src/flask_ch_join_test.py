'''
high level support for functions
'''
import requests
from echo_http_test import url

# 1 - invalid channel, 2 - private channel, 3 - if the user already in channel
def test_invalid_no_channel(url):
    ''' tests an invalid channel id, ensures input error is raised'''
    # Clear the Data frame for black box testing
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'z5309388@unsw.edu.au',
        'password': 'Password1',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload = response.json()
    join_input = {'token': register_payload['token'], 'channel_id': 1}
    response = requests.post(f"{url}/channel/join", json=join_input)
    # join_payload = response.json()
    assert response.status_code == 400


def test_invalid_private(url):
    ''' private channel raise error '''
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'z5309388@unsw.edu.au',
        'password': 'Password1',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload1 = response.json()
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'z5309389@unsw.edu.au',
        'password': 'Password2',
        'name_first':'Kangnan',
        'name_last': 'Wang'
        })
    register_payload2 = response.json()

    response = requests.post(f"{url}/channels/create", json={
        'token': register_payload1['token'],
        'name': "James' Channel",
        'is_public': False
    })
    channels_payload = response.json()
    join_input = {
        'token': register_payload2['token'],
        'channel_id': channels_payload['channel_id']
    }
    response = requests.post(f"{url}/channel/join", json=join_input)
    assert response.status_code == 400

def test_valid(url):
    ''' valid channel join'''
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'z5309388@unsw.edu.au',
        'password': 'Password1',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload1 = response.json()
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'z5309389@unsw.edu.au',
        'password': 'Password2',
        'name_first':'Kangnan',
        'name_last': 'Wang'
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
    response = requests.get(f"{url}/channel/details", params={
        'token': register_payload1['token'],
        'channel_id': channels_payload['channel_id']
    })

    details_payload = response.json()

    assert details_payload['all_members'] == [
        {
            'u_id': 1,
            'name_first' : 'James',
            'name_last' : 'Turner'
        },
        {
            'u_id': 2,
            'name_first' : 'Kangnan',
            'name_last' : 'Wang'
        }
    ]

    assert details_payload['owner_members'] == [
        {
            'u_id': 1,
            'name_first' : 'James',
            'name_last' : 'Turner'
        }
    ]
