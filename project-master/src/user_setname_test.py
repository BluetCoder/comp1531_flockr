""" Imports """
import pytest
from structure import Data
from user import user_profile_setname
from error import InputError, AccessError
from other import clear
import auth

def test_valid_setname():
    """ testing user_profile_setname with valid inputs """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    user_profile_setname(result['token'], "Johnny", "Smithy")
    assert Data['users'][0]['name_first'] == 'Johnny'
    assert Data['users'][0]['name_last'] == 'Smithy'

def test_invalid_token():
    """ testing user_profile_setname with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    auth.auth_logout(result['token'])
    with pytest.raises(AccessError):
        assert user_profile_setname(result['token'], "Johnny", "Smithy")

def test_invalid_first_short():
    """ testing user_profile_setname with short firstname """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    with pytest.raises(InputError):
        assert user_profile_setname(result['token'], "j", "Smithy")

def test_invalid_first_long():
    """ testing user_profile_setname with long firstname """
    clear()
    auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    result = auth.auth_register('test02@gmail.com', '111111', 'JoHn', 'Smith')
    first = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    with pytest.raises(InputError):
        assert user_profile_setname(result['token'], first, "Smithy")

def test_invalid_last_short():
    """ testing user_profile_setname with short lastname """
    clear()
    auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    result = auth.auth_register('test02@gmail.com', '111111', 'JoHn', 'Smith')
    with pytest.raises(InputError):
        assert user_profile_setname(result['token'], "Johnny", "S")

def test_invalid_last_long():
    """ testing user_profile_setname with long lastname """
    clear()
    auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    result = auth.auth_register('test02@gmail.com', '111111', 'JoHn', 'Smith')
    last = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    with pytest.raises(InputError):
        assert user_profile_setname(result['token'], "Johnny", last)
