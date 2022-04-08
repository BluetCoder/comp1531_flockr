'''
high level support for functions
'''
import requests
from echo_http_test import url

def test_valid_handle_change(url):
    """ testing user_profile_sethandle with valid inputs """
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
    payload2 = response.json()
    sethandle_input = {'token': payload1['token'], 'handle_str': "babyli123"}
    response = requests.put(f"{url}/user/profile/sethandle", json=sethandle_input)
    sethandle_payload = response.json()
    assert sethandle_payload == {}
    
    profile_input = {'token': payload2['token'], 'u_id': payload1['u_id']}
    #response = requests.get(f"{url}/user/profile", json=profile_input)
    response = requests.get(f"{url}/user/profile",params=profile_input)
    profile_payload = response.json()

    assert profile_payload['user']['handle_str'] == 'babyli123'

def test_handle_long(url):
    """ testing user_profile_setemail with long handle length (20+ characters) """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()
    
    sethandle_input = {'token': payload1['token'], 'handle_str': "virgilvandijkwashackedbypickford"}
    response = requests.put(f"{url}/user/profile/sethandle", json=sethandle_input)
    sethandle_payload = response.json()
    assert sethandle_payload['code'] == 400

def test_handle_short(url):
    """ testing user_profile_setname with short handle length (<3) """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()
    
    sethandle_input = {'token': payload1['token'], 'handle_str': "nu"}
    response = requests.put(f"{url}/user/profile/sethandle", json=sethandle_input)
    sethandle_payload = response.json()
    assert sethandle_payload['code'] == 400

def test_handle_taken(url):
    """ testing user_profile_sethandle with valid inputs """
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
    payload2 = response.json()
    sethandle_input = {'token': payload1['token'], 'handle_str': "babyli123"}
    response = requests.put(f"{url}/user/profile/sethandle", json=sethandle_input)
    sethandle_payload = response.json()
    assert sethandle_payload == {}
    
    sethandle_input2 = {'token': payload2['token'], 'handle_str': "babyli123"}
    response = requests.put(f"{url}/user/profile/sethandle", json=sethandle_input2)
    sethandle_payload2 = response.json()
    assert sethandle_payload2['code'] == 400

def test_invalid_token(url):
    """ testing user_profile_setname with short firstname """
    response = requests.delete(f"{url}/clear", json={})
    sethandle_input = {'token': "abc", 'handle_str': "babyli123"}
    response = requests.put(f"{url}/user/profile/sethandle", json=sethandle_input)
    sethandle_payload = response.json()
    assert sethandle_payload['code'] == 400
