""" Imports """
import pytest
from structure import Data
from user import user_profile_sethandle
from error import InputError, AccessError
from other import clear
import auth

def test_valid_handle_change():
    """ testing user_profile_sethandle with valid inputs """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    newhandle = "babyli123"
    user_profile_sethandle(result['token'], newhandle)
    assert Data['users'][0]['handle_str'] == 'babyli123'

def test_handle_long():
    """ testing user_profile_setemail with long handle length (20+ characters) """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    newhandle = "virgilvandijkwashackedbypickford"
    with pytest.raises(InputError):
        user_profile_sethandle(result['token'], newhandle)

def test_handle_short():
    """ testing user_profile_setname with short handle length (<3) """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    newhandle = "nu"
    with pytest.raises(InputError):
        assert user_profile_sethandle(result['token'], newhandle)

def test_handle_taken():
    """ testing user_profile_sethandle with valid inputs """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    result2 = auth.auth_register('test02@gmail.com', '111111', 'Sam', 'Smith')
    newhandle = "babyli123"
    user_profile_sethandle(result['token'], newhandle)
    with pytest.raises(InputError):
        user_profile_sethandle(result2['token'], newhandle)

def test_invalid_token():
    """ testing user_profile_setname with short firstname """
    clear()
    with pytest.raises(AccessError):
        assert user_profile_sethandle("abc", "email")
