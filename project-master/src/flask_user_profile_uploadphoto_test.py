'''
high level support for functions
'''
import requests
from echo_http_test import url

def test_valid_profile_uploadphoto(url):
    """ testing user_profile_uploadphoto with valid input """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    register_payload = response.json()
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpg"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : register_payload['token'],
        'img_url': img_url,
        'x_start': 0,
        'x_end': 100,
        'y_start': 0,
        'y_end': 100
        })
    payload = response.json()
    assert payload == {}

def test_invalid_token(url):
    """ testing user_profile_uploadphoto with invalid token """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    img_url = "https://upload.wikimedia.org/wikipedia/commons/4/41/Sunflower_from_Silesia2.jpg"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : "fail",
        'img_url': img_url,
        'x_start': 0,
        'x_end': 100,
        'y_start': 0,
        'y_end': 100
        })
    assert response.status_code == 400

def test_invalid_xstart_greater_xend(url):
    """ xstart greater than xend """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    img_url = "https://upload.wikimedia.org/wikipedia/commons/4/41/Sunflower_from_Silesia2.jpg"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : payload['token'],
        'img_url': img_url,
        'x_start': 1,
        'x_end': 0,
        'y_start': 0,
        'y_end': 1
        })
    assert response.status_code == 400

def test_invalid_ystart_greater_yend(url):
    """ ystart greater than yend """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    img_url = "https://upload.wikimedia.org/wikipedia/commons/4/41/Sunflower_from_Silesia2.jpg"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : payload['token'],
        'img_url': img_url,
        'x_start': 0,
        'x_end': 1,
        'y_start': 10,
        'y_end': 0
        })
    assert response.status_code == 400

def test_invalid_xstart_big(url):
    """ invalid xstart too big """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    img_url = "https://upload.wikimedia.org/wikipedia/commons/4/41/Sunflower_from_Silesia2.jpg"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : payload['token'],
        'img_url': img_url,
        'x_start': 10000,
        'x_end': 10010,
        'y_start': 0,
        'y_end': 1
        })
    assert response.status_code == 400

def test_invalid_xend_big(url):
    """ xend too big """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    img_url = "https://upload.wikimedia.org/wikipedia/commons/4/41/Sunflower_from_Silesia2.jpg"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : payload['token'],
        'img_url': img_url,
        'x_start': 0,
        'x_end': 10010,
        'y_start': 0,
        'y_end': 1
        })
    assert response.status_code == 400

def test_invalid_ystart_big(url):
    """ ystart too big """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    img_url = "https://upload.wikimedia.org/wikipedia/commons/4/41/Sunflower_from_Silesia2.jpg"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : payload['token'],
        'img_url': img_url,
        'x_start': 0,
        'x_end': 1,
        'y_start': 10000,
        'y_end': 10010
        })
    assert response.status_code == 400

def test_invalid_yend_big(url):
    """ y_end too big """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    img_url = "https://upload.wikimedia.org/wikipedia/commons/4/41/Sunflower_from_Silesia2.jpg"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : payload['token'],
        'img_url': img_url,
        'x_start': 0,
        'x_end': 1,
        'y_start': 0,
        'y_end': 10000
        })
    assert response.status_code == 400

def test_invalid_img_url(url):
    """ Invalid img_url """
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    img_url = "https://upload.wikimedia.org/wikipedia/commons/4/41/Sunflower_from_Silesia2.jpg.fail"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : payload['token'],
        'img_url': img_url,
        'x_start': 0,
        'x_end': 100,
        'y_start': 0,
        'y_end': 100
        })
    assert response.status_code == 400

def test_invalid_not_jpg(url):
    ''' img_url does not give jpg '''
    response = requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : 'test01@gmail.com',
        'password': '111111',
        'name_first':'John',
        'name_last': 'Smith'
        })
    payload = response.json()
    img_url = "https://www.edigitalagency.com.au/wp-content/uploads/new-instagram-logo-png-transparent-light-858x857.png"
    response = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : payload['token'],
        'img_url': img_url,
        'x_start': 0,
        'x_end': 100,
        'y_start': 0,
        'y_end': 100
        })
    assert response.status_code == 400

