import urllib.request
import sys
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
    
    assert user_profile_uploadphoto(result['token'], img_url, 0, 0, 50, 50) == {}