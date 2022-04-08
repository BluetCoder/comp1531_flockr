""" Imports """
import pytest
import jwt
import auth
from structure import SECRET
from error import InputError
from other import clear
from helper import encode_token

def test_empty():
    """ Test empty input """
    clear()
    with pytest.raises(InputError):
        assert auth.auth_login("", "")

def test_invalid_email_01():
    """ Test invalid email input """
    clear()
    with pytest.raises(InputError):
        assert auth.auth_login("abc", "abc")

def test_invalid_email_02():
    """ Test invalid email input 02 """
    clear()
    with pytest.raises(InputError):
        assert auth.auth_login("ankitrai326.com", "abc")

def test_wrong_email_01():
    """ Test wrong email input """
    clear()
    register_output = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    auth.auth_logout(register_output['token'])
    with pytest.raises(InputError):
        assert auth.auth_login("my.ownsit@ourearth.org", "111111")

def test_wrong_password_01():
    """ Test wrong email input """
    clear()
    register_output = auth.auth_register('susanshuwanguo@gmail.com', '111111', 'Shuwan', 'Guo')
    auth.auth_logout(register_output['token'])
    with pytest.raises(InputError):
        assert auth.auth_login("susanshuwanguo@gmail.com", "abc")

def test_valid_01():
    """ Test valid login """
    clear()
    register_output = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    auth.auth_logout(register_output['token'])
    result = auth.auth_login("susanshuwanguo@gmail.com", "123456")
    assert result['u_id'] == 1
    assert result['token'] == encode_token(result['u_id'])

def test_valid_02():
    """ Test valid login 02 """
    clear()
    register_output01 = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    auth.auth_logout(register_output01['token'])
    register_output02 = auth.auth_register('henry.zhang@gmail.com', '345678', 'Henry', 'Zhang')
    auth.auth_logout(register_output02['token'])
    result = auth.auth_login("henry.zhang@gmail.com", "345678")
    assert result['u_id'] == 2
    assert result['token'] == encode_token(result['u_id'])
