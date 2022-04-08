''' high level support functions '''
import requests
from echo_http_test import url
from helper import flask_set_up


def test_empty_input(url):
    ''' Test with empty input '''
    # use requests to clear, then request channel details with empty input
    response = requests.delete(f"{url}/clear", json={})
    response = requests.get(f"{url}/channel/details", params={
        "token": "",
        "channel_id": ""
    })
    #assert the response is 400, bad request
    assert response.status_code == 400

def test_not_registered(url):
    ''' Test with invalid token '''
    # use requests to clear, then request channel details with an invalid token
    response = requests.delete(f"{url}/clear", json={})
    response = requests.get(f"{url}/channel/details", params={
        "token": "abc",
        "channel_id": ""
    })
    #assert the response is 400, bad request
    assert response.status_code == 400

def test_wrong_channel(url):
    ''' Test with wrong input channel_id '''
    # flask_set_up clears, and registers a user, and creates a channel
    result = flask_set_up(url)

    #creates a channel
    response = requests.post(f"{url}/channels/create", json={
        "token": result['token'],
        "name": "ahaha",
        "is_public": True
    })
    # requests details, but channel_id is invalid
    response = requests.get(f"{url}/channel/details", params={
        "token": result['token'],
        "channel_id": 5
    })
    # assert response is 400, bad request
    assert response.status_code == 400

def test_not_in_the_channel(url):
    ''' Test with user not being in the channel '''
    # flask_set_up clears, and registers a user, and creates a channel
    result = flask_set_up(url)
    #register new user 2
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test02@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    register_payload2 = response.json()
    #create  a channel with new user 1
    response = requests.post(f"{url}/channels/create", json={
        "token": result['token'],
        "name": "ahaha",
        "is_public": True
    })
    create_payload = response.json()
    # request channel_details with new user 2
    response = requests.get(f"{url}/channel/details", params={
        "token": register_payload2['token'],
        "channel_id": create_payload['channel_id']
    })
    # assert response is 400, bad request
    assert response.status_code == 400

def test_valid_input(url):
    ''' Test with valid input and one member in channel '''
    # flask_set_up clears, and registers a user, and creates a channel
    result = flask_set_up(url)
    # create a new channel
    response = requests.post(f"{url}/channels/create", json={
        "token": result['token'],
        "name": "ahaha",
        "is_public": True
    })
    create_payload = response.json()
    # request its details
    response = requests.get(f"{url}/channel/details", params={
        "token": result['token'],
        "channel_id": create_payload['channel_id']
    })

    details_payload = response.json()
    # correct assertions
    print(details_payload)
    assert details_payload['name'] == 'ahaha'
    assert details_payload['owner_members'] == [
        {
            'u_id': 1,
            'name_first' : 'John',
            'name_last' : 'Smith'
        }
    ]
    assert details_payload['all_members'] == [
        {
            'u_id': 1,
            'name_first' : 'John',
            'name_last' : 'Smith'
        }
    ]
