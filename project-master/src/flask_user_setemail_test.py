'''
high level support for functions
'''
import re
import signal
from time import sleep
from subprocess import Popen, PIPE
import requests
import pytest

@pytest.fixture
def url():
    ''' Sets up a server '''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_valid_email_change(url):
    """ testing user_profile_setemail with valid inputs """
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

    setemail_input = {'token': payload1['token'], 'email': 'test03@gmail.com'}

    response = requests.put(f"{url}/user/profile/setemail", json=setemail_input)
    setemail_payload = response.json()
    assert setemail_payload == {}

    profile_input = {'token': payload2['token'], 'u_id': payload1['u_id']}
    #response = requests.get(f"{url}/user/profile", json=profile_input)
    response = requests.get(f"{url}/user/profile",params=profile_input)
    profile_payload = response.json()

    assert profile_payload['user']['email'] == 'test03@gmail.com'

def test_invalid_email_regex(url):
    """ testing user_profile_setemail with invalid email """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload1 = response.json()

    setemail_input = {'token': payload1['token'], 'email': "c at ch me outside"}
    response = requests.put(f"{url}/user/profile/setemail", json=setemail_input)
    setemail_payload = response.json()
    assert setemail_payload['code'] == 400

def test_email_in_use(url):
    """ testing user_profile_setname with short firstname """
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

    setemail_input = {'token': payload1['token'], 'email': 'test02@gmail.com'}

    response = requests.put(f"{url}/user/profile/setemail", json=setemail_input)
    setemail_payload = response.json()
    assert setemail_payload['code'] == 400

def test_invalid_token(url):
    """ testing user_profile_setname with short firstname """
    response = requests.delete(f"{url}/clear", json={})
    setemail_input = {'token': "abc", 'email': 'test02@gmail.com'}
    response = requests.put(f"{url}/user/profile/setemail", json=setemail_input)
    setemail_payload = response.json()
    assert setemail_payload['code'] == 400
