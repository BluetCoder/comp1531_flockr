''' high level support functions '''
import requests
from echo_http_test import url

def test_no_channel_created_by_user(url):
    '''testing function for channels_list'''
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

    #response = requests.get(f"{url}/channels/list", json={
    #    "token": token
    #})
    payload = requests.get(f"{url}/channels/list",params={'token':token},).json()

    #payload = response.json()
    assert payload['channels'] == []

def test_one_channel_created_by_user(url):
    '''testing function for channels_list'''
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

    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "coding",
        "is_public": True
    })

    payload = response.json()

    payload = requests.get(f"{url}/channels/listall",params={'token':token},).json()
    
    print(payload)
    assert payload['channels'][0]['name'] == "coding"
    assert payload['channels'][0]['channel_id'] == 1

def test_multiple_channels_created(url):
    '''testing function for channels_create, invalid name'''
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

    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "channelone",
        "is_public": "True"
    })

    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "channeltwo",
        "is_public": "True"
    })

    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "channelthree",
        "is_public": "True"
    })

    #response = requests.get(f"{url}/channels/listall", json={
    #    "token": token
    #})

    #payload = response.json()
    payload = requests.get(f"{url}/channels/listall",params={'token':token},).json()
    assert payload['channels'][0]['name'] == "channelone"
    assert payload['channels'][0]['channel_id'] == 1
    assert payload['channels'][1]['name'] == "channeltwo"
    assert payload['channels'][1]['channel_id'] == 2
    assert payload['channels'][2]['name'] == "channelthree"
    assert payload['channels'][2]['channel_id'] == 3

def test_multiple_channels_created_two_users(url):
    ''' one more test with two users logged in and three channels created'''
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

    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test02@gmail.com',
        'password': '111111',
        'name_first':'Virgil',
        'name_last': 'Van Dijk'
        })
    payload = response.json()

    token_2 = payload['token']
    u_id = payload['u_id']
    assert u_id == 2

    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "channelone",
        "is_public": "True"
    })

    response = requests.post(f"{url}/channels/create", json={
        "token": token_2,
        "name": "channeltwo",
        "is_public": "True"
    })

    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "channelthree",
        "is_public": "True"
    })

    #response = requests.get(f"{url}/channels/listall", json={
    #    "token": token
    #})

    #payload = response.json()
    payload = requests.get(f"{url}/channels/listall",params={'token':token},).json()
    assert payload['channels'][0]['name'] == "channelone"
    assert payload['channels'][0]['channel_id'] == 1
    assert payload['channels'][1]['name'] == "channeltwo"
    assert payload['channels'][1]['channel_id'] == 2
    assert payload['channels'][2]['name'] == "channelthree"
    assert payload['channels'][2]['channel_id'] == 3


def test_invalid_token(url):
    '''testing function for channels_create, invalid name'''
    response = requests.delete(f"{url}/clear", json={})

    token = "thisisnotatoken"

    response = requests.get(f"{url}/channels/listall", json={
        "token": token
    })

    payload = response.json()
    assert payload['code'] == 400
