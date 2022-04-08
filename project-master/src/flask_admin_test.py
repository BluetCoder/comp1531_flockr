'''
high level support for functions
'''
import requests
from echo_http_test import url
from helper import flask_set_up

def test_valid(url):
    ''' valid permission change '''
    result = flask_set_up(url)
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'z5309388@unsw.edu.au',
        'password': 'password1',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload2 = response.json()
    
    response = requests.post(f"{url}/admin/userpermission/change", json={
        "token" : result['token'],
        'u_id': register_payload2['u_id'],
        'permission_id': 1
        })
    admin_payload = response.json()
    assert admin_payload == {}

    response = requests.post(f"{url}/channels/create", json={
        "token": result['token'],
        "name": "Test",
        "is_public": False
    })
    create_payload = response.json()
    response = requests.post(f"{url}/channel/join", json={
        "token" : register_payload2['token'],
        'channel_id': create_payload['channel_id']
        })
    join_payload = response.json()
    assert join_payload == {}

def test_not_owner(url):
    ''' given token doesn't refer to owner, can't change permissions '''
    result = flask_set_up(url)
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'z5309388@unsw.edu.au',
        'password': 'password1',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload2 = response.json()
    
    response = requests.post(f"{url}/admin/userpermission/change", json={
        "token" : register_payload2['token'],
        'u_id': result['u_id'],
        'permission_id': 1
        })
    assert response.status_code == 400

def test_own_permission(url):
    ''' user can't change own permissions'''
    result = flask_set_up(url)

    response = requests.post(f"{url}/admin/userpermission/change", json={
        "token" : result['token'],
        'u_id': result['u_id'],
        'permission_id': 1
        })
    assert response.status_code == 400

def test_uid_invalid(url):
    ''' u_id refers to invalid user '''
    result = flask_set_up(url)
    response = requests.post(f"{url}/admin/userpermission/change", json={
        "token" : result['token'],
        'u_id': 69,
        'permission_id': 1
        })
    assert response.status_code == 400

def test_invalid_perm_id(url):
    ''' permission id is not 1 or 2 '''
    result = flask_set_up(url)
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'z5309388@unsw.edu.au',
        'password': 'password1',
        'name_first':'James',
        'name_last': 'Turner'
        })
    register_payload2 = response.json()
    
    response = requests.post(f"{url}/admin/userpermission/change", json={
        "token" : result['token'],
        'u_id': register_payload2['u_id'],
        'permission_id': 3
        })
    assert response.status_code == 400
