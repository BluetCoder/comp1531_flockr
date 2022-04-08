'''
high level support for functions
'''
import requests
from echo_http_test import url

def test_bad_email1(url):
    '''wrong email type 1'''
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'james.owen.turner@gmail.com',
        'password': '111111',
        'name_first':'James',
        'name_last': 'Turner'
        })
    response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'james.owen.turnerr@gmail.com'
    })
    assert response.status_code == 400


def test_bad_email2(url):
    '''wrong email type 2'''
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'james.owen.turner@gmail.com',
        'password': '111111',
        'name_first':'James',
        'name_last': 'Turner'
        })
    response = requests.post(f"{url}/auth/passwordreset/request", json={
        'email': 'james.owen.turnerr@gmailcom'
    })
    assert response.status_code == 400
