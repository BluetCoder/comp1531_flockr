'''
high level support for functions
'''
import requests
from echo_http_test import url
from structure import Data

def test_invalid_code(url):
    ''' code is not in Database '''
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'james.owen.turner@gmail.com',
        'password': '111111',
        'name_first':'James',
        'name_last': 'Turner'
        })
    response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'james.owen.turner@gmail.com'
    })
    response = requests.post(f"{url}/auth/passwordreset/reset", json={
        'reset_code': 'CdkJbHc69',
        'new_password': 'Password2'
    })
    assert response.status_code == 400

def test_invalid_code2(url):
    ''' code is not in Database '''
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'james.owen.turner@gmail.com',
        'password': '111111',
        'name_first':'James',
        'name_last': 'Turner'
        })
    response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'james.owen.turner@gmail.com'
    })
    response = requests.post(f"{url}/auth/passwordreset/reset", json={
        'reset_code': 'asdfuibaasdkcnansdf',
        'new_password': 'Password2'
    })
    assert response.status_code == 400
