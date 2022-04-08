'''
high level support for functions
'''
import requests
from echo_http_test import url

def test_invalid_token(url):
    """ testing user_profile with invalid token """
    #response = requests.get(f"{url}/users/all", json={'token': 'fail'})
    #payload = response.json()
    response = requests.get(f"{url}/users/all",params={'token':'fail'})
    #assert payload['code'] == 400

    assert response.status_code == 400

def test_valid_users_all(url):
    ''' testing valid token with users_all '''
    #token = setup(url)
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'Aha',
        'name_last': 'Ahaha'
        })
    payload = response.json()

    token = payload['token']

    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test02@gmail.com',
        'password': '111111',
        'name_first':'Emm',
        'name_last': 'Emmmm'
        })
    payload = requests.get(f"{url}/users/all",params={'token':token}).json()
    assert payload['users'] == [{
            'u_id': 1,
            'email': 'test01@gmail.com',
            'name_first': 'Aha',
            'name_last': 'Ahaha',
            'handle_str': 'ahaahaha',
            'profile_img_url': None
        },
        {
            'u_id': 2, 
            'email': 'test02@gmail.com',
            'name_first': 'Emm',
            'name_last':'Emmmm',
            'handle_str': 'emmemmmm',
            'profile_img_url': None
        }
    ]
