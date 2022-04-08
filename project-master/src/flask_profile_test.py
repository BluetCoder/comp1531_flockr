'''
high level support for functions
'''
import requests
from echo_http_test import url
from structure import Data

def test_valid_profile(url):
    """ testing user_profile with valid inputs """
    # requests to clear and register a new user
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()
    # register a new user 2
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test02@gmail.com',
        'password': '111111',
        'name_first':'JoHn',
        'name_last': 'Smith'
        })
    payload2 = response.json()
    # check user_1 profile, from user_2 token
    input_dict = {'token': payload2['token'], 'u_id': payload1['u_id']}
    response = requests.get(f"{url}/user/profile", params=input_dict)
    profile_payload = response.json()
    # check user_1 profile matches the auth_register
    assert profile_payload['user']['u_id'] == 1
    assert profile_payload['user']['email'] == 'test01@gmail.com'
    assert profile_payload['user']['name_first'] == 'John'
    assert profile_payload['user']['name_last'] == 'Smith'
    assert profile_payload['user']['handle_str'] == 'johnsmith'

def test_invalid_token(url):
    """ testing user_profile with invalid token """
    # requests to clear and register a user
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()
    # with an invalid token, try and request user-profile of user1
    input_dict = {'token': "abc", 'u_id': payload1['u_id']}
    response = requests.get(f"{url}/user/profile", json=input_dict)
    profile_payload = response.json()
    # assert 400 error, bad request
    assert profile_payload['code'] == 400

def test_invalid_u_id(url):
    """ testing user_profile with invalid u_id """
    # requests to clear and register a user
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test02@gmail.com',
        'password': '111111',
        'name_first':'JoHn',
        'name_last': 'Smith'
        })
    # with a valid token, try and request user-profile of a non-existent user
    input_dict = {'token': payload1['token'], 'u_id': 5}
    response = requests.get(f"{url}/user/profile", json=input_dict)
    profile_payload = response.json()
    # assert 400 error, bad request
    assert profile_payload['code'] == 400
