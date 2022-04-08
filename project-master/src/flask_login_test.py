'''
high level support for functions
'''
import requests
from echo_http_test import url

def test_login(url):
    '''testing function for auth_login'''
    # requests to clear and register a new user
    response = requests.delete(f"{url}/clear", json={})
    email = 'test01@gmail.com'
    password = '111111'
    response = requests.post(f"{url}/auth/register", json={
        "email" : email,
        'password': password,
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    u_id = payload['u_id']
    token = payload['token']
    assert u_id == 1
    response = requests.post(f"{url}/auth/logout", json={
        "token": token
    })
    logout_payload = response.json()
    assert logout_payload['is_success'] is True
    response = requests.post(f"{url}/auth/login", json={
        "email" : email,
        "password" : password
    })
    login_payload = response.json()
    assert login_payload['token'] == token

def test_invalid_email(url):
    '''testing invalid email as input'''
    # requests to clear and login a new user with invalid email
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/login", json={
        "email" : 'invalidemailaddress',
        'password': '111111'
        })
    payload = response.json()
    assert payload['code'] == 400

def test_used_email(url):
    '''testing used email as input'''
    # requests to clear and double login a user
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/login", json={
        "email" : 'test01@gmail.com',
        'password': '111111'
        })
    response = requests.post(f"{url}/auth/login", json={
        "email" : 'test01@gmail.com',
        'password': '111111'
        })
    payload = response.json()
    # assert request returned 400, bad response
    assert payload['code'] == 400

def test_password(url):
    '''testing improper password as input'''
    # requests to clear and  login a user with invalid login
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/login", json={
        "email" : '222222@gmail.com',
        'password': '1'
        })
    payload = response.json()
    # assert request returned 400, bad response
    assert payload['code'] == 400
