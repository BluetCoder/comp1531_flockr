""" Imports """
import pytest
from structure import Data
from user import user_profile_setemail
from error import InputError, AccessError
from other import clear
import auth

def test_valid_email_change():
    """ testing user_profile_setemail with valid inputs """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    email = "test02@gmail.com"
    user_profile_setemail(result['token'], email)
    assert Data['users'][0]['email'] == 'test02@gmail.com'

def test_invalid_email_regex():
    """ testing user_profile_setemail with invalid email """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    email = "c at ch me outside"
    with pytest.raises(InputError):
        assert user_profile_setemail(result['token'], email)

def test_email_in_use():
    """ testing user_profile_setname with short firstname """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    result = auth.auth_register('test02@gmail.com', '111111', 'Jane', 'Doe')
    email = 'test02@gmail.com'
    with pytest.raises(InputError):
        assert user_profile_setemail(result['token'], email)

def test_invalid_token():
    """ testing user_profile_setname with short firstname """
    clear()
    with pytest.raises(AccessError):
        assert user_profile_setemail("abc", "email")
