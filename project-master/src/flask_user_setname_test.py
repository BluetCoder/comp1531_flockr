'''
high level support for functions
'''
import requests
from echo_http_test import url

def test_valid_setname(url):
    """ testing user_profile_setname with valid inputs """
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
    
    profile_dict = {'token': payload2['token'], 'u_id': payload1['u_id']}
    setname_dict = {'token': payload1['token'], 'name_first': 'Johnny', 'name_last': 'Smithy'}
    
    response = requests.put(f"{url}/user/profile/setname", json=setname_dict)
    setname_payload = response.json()
    assert setname_payload == {}
    
    #response = requests.get(f"{url}/user/profile", json=profile_dict)
    response = requests.get(f"{url}/user/profile",params=profile_dict)
    profile_payload = response.json()

    assert profile_payload['user']['u_id'] == 1
    assert profile_payload['user']['email'] == 'test01@gmail.com'
    assert profile_payload['user']['name_first'] == 'Johnny'
    assert profile_payload['user']['name_last'] == 'Smithy'
    assert profile_payload['user']['handle_str'] == 'johnsmith'

def test_invalid_token(url):
    """ testing user_profile_setname with invalid token """
    response = requests.delete(f"{url}/clear", json={})
    setname_dict = {'token': 'fail', 'name_first': 'Johnny', 'name_last': 'Smithy'}
    response = requests.put(f"{url}/user/profile/setname", json=setname_dict)
    setname_payload = response.json()
    assert setname_payload['code'] == 400

def test_invalid_first_short(url):
    """ testing user_profile_setname with short firstname """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()
    setname_dict = {'token': payload1['token'], 'name_first': 'j', 'name_last': 'Smithy'}
    response = requests.put(f"{url}/user/profile/setname", json=setname_dict)
    setname_payload = response.json()
    assert setname_payload['code'] == 400

def test_invalid_first_long(url):
    """ testing user_profile_setname with long firstname """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()
    first = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    setname_dict = {'token': payload1['token'], 'name_first': first, 'name_last': 'Smithy'}
    response = requests.put(f"{url}/user/profile/setname", json=setname_dict)
    setname_payload = response.json()
    assert setname_payload['code'] == 400

def test_invalid_last_short(url):
    """ testing user_profile_setname with short lastname """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()
    setname_dict = {'token': payload1['token'], 'name_first': 'Johnny', 'name_last': 'S'}
    response = requests.put(f"{url}/user/profile/setname", json=setname_dict)
    setname_payload = response.json()
    assert setname_payload['code'] == 400

def test_invalid_last_long(url):
    """ testing user_profile_setname with long lastname """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()
    last = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    setname_dict = {'token': payload1['token'], 'name_first': 'Johnny', 'name_last': last}
    response = requests.put(f"{url}/user/profile/setname", json=setname_dict)
    setname_payload = response.json()
    assert setname_payload['code'] == 400

