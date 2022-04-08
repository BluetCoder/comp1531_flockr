'''
high level support for functions
'''
import requests
from echo_http_test import url
from helper import encode_token

def test_logout(url):
    '''testing function for auth_logout'''
    # requests to clear and register a new user
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
    # request a normal logout
    response = requests.post(f"{url}/auth/logout", json={
        "token": token
    })
    logout_payload = response.json()
    # assert logout succeeded
    assert logout_payload['is_success'] is True

def test_invalid_token(url):
    '''testing invalid email as input'''
    # clear, and logout with an invalid token
    response = requests.delete(f"{url}/clear", json={})
    token = "tokenless"
    response = requests.post(f"{url}/auth/logout", json={
        "token" : token
    })
    payload = response.json()
    # assert bad response, response returns 400
    assert payload['code'] == 400
