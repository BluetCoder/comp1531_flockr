'''
high level support for functions
'''
import requests
from echo_http_test import url
from helper import encode_token

def test_register(url):
    '''testing function for auth_register'''
    # requests to clear and register a new user
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    # assert that u_id and token are correct
    assert payload['u_id'] == 1
    assert payload['token'] == encode_token(payload['u_id'])
    # need to add users_all function to check if the user is registered

def test_invalid_email(url):
    '''testing invalid email as input'''
    # requests to clear and register a new user
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'invalidemailaddress',
        'password': '111111',
        'name_first': 'Alice',
        'name_last': 'Green'
        })
    payload = response.json()
    # assert 400 error, bad request
    assert payload['code'] == 400

def test_used_email(url):
    '''testing used email as input'''
    # requests to clear and register a new user
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first': 'John',
        'name_last': 'Smith'
        })
    # request to register with a used email
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first': 'Shuwan',
        'name_last': 'Guo'
        })
    payload = response.json()
    # assert 400 error, bad request
    assert payload['code'] == 400

def test_password(url):
    '''testing improper password as input'''
    # requests to clear and register a new user, using an invalid password
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : '222222@gmail.com',
        'password': '1',
        'name_first': 'Alice',
        'name_last': 'Green'
        })
    payload = response.json()
    # assert 400 error, bad request
    assert payload['code'] == 400

def test_first_name(url):
    '''testing improper first name as input'''
    # requests to clear and register a new user, using an invalid first name
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : '333333@gmail.com',
        'password': '456789',
        'name_first': 'Aliceaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'name_last': 'Green'
        })
    payload = response.json()
    # assert 400 error, bad request
    assert payload['code'] == 400

def test_last_name(url):
    '''testing improper last name as input'''
    # requests to clear and register a new user, using an invalid last name
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : '444444@gmail.com',
        'password': '345678',
        'name_first': 'John',
        'name_last': ''
        })
    payload = response.json()
    # assert 400 error, bad request
    assert payload['code'] == 400
