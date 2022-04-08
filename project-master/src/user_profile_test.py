""" Imports """
import pytest
from user import user_profile
from error import InputError, AccessError
from other import clear
import auth

def test_valid_profile():
    """ testing user_profile with valid inputs """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    result02 = auth.auth_register('test02@gmail.com', '111111', 'JoHn', 'Smith')
    user = user_profile(result02['token'], result['u_id'])
    assert user['user']['u_id'] == 1
    assert user['user']['email'] == 'test01@gmail.com'
    assert user['user']['name_first'] == 'John'
    assert user['user']['name_last'] == 'Smith'
    assert user['user']['handle_str'] == 'johnsmith'

def test_invalid_token():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    result02 = auth.auth_register('test02@gmail.com', '111111', 'JoHn', 'Smith')
    auth.auth_logout(result02['token'])
    with pytest.raises(AccessError):
        assert user_profile(result02['token'], result['u_id'])

def test_invalid_u_id():
    """ testing user_profile with invalid u_id """
    clear()
    auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    result02 = auth.auth_register('test02@gmail.com', '111111', 'JoHn', 'Smith')
    with pytest.raises(InputError):
        assert user_profile(result02['token'], 5)
