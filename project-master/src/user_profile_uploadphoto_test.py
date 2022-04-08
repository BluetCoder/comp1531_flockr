""" Imports """
import pytest
from user import user_profile_uploadphoto
from error import InputError, AccessError
from other import clear
import auth

def test_valid_profile_uploadphoto():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    #img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg"
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpg"
    
    assert user_profile_uploadphoto(result['token'], img_url, 0, 0, 1, 1) == {}
'''
def test_invalid_token():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    auth.auth_logout(result['token'])
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg"
    with pytest.raises(AccessError):
        assert user_profile_uploadphoto(result['token'], img_url, 0, 0, 1, 1)

def test_invalid_xstart_greater_xend():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(result['token'], img_url, 1, 0, 0, 1)

def test_invalid_ystart_greater_yend():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(result['token'], img_url, 0, 1, 0, 0)

def test_invalid_ystart_greater_yend():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(result['token'], img_url, 0, 1, 0, 0)

def test_invalid_xstart_big():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(result['token'], img_url, 1000, 1, 1001, 1)

def test_invalid_xend_big():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(result['token'], img_url, 0, 1, 1000, 1)

def test_invalid_ystart_big():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(result['token'], img_url, 0, 1000, 1, 1001)

def test_invalid_yend_big():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(result['token'], img_url, 0, 0, 1, 1001)

def test_invalid_img_url():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    img_url = "https://personal.psu.edu/xqz5228/jpg.jpghttps://personal.psu.edu/xqz5228/jpg.jpg.fail"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(result['token'], img_url, 0, 0, 1, 1)

def test_invalid_not_jpg():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    img_url = "https://www.edigitalagency.com.au/wp-content/uploads/new-instagram-logo-png-transparent-light-858x857.png"
    with pytest.raises(InputError):
        assert user_profile_uploadphoto(result['token'], img_url, 0, 0, 1, 1)
'''
