'''
Testing function to confirm absence of bugs in auth function auth_logout
'''
import pytest
import jwt
from auth import auth_logout
from auth import auth_register
from structure import Data, SECRET
from error import AccessError
from other import clear
from helper import encode_token


def test_valid_token():
    ''' tests if a valid token can be logged out without bugs '''
    clear()
    email_test = "z5309388@unsw.edu.au"
    password_test = 'Password1'
    name_first_test = 'James'
    name_last_test = 'Turner'
    register_out = auth_register(email_test, password_test, name_first_test, name_last_test)
    assert auth_logout(register_out['token'])['is_success'] == True
    assert Data['users'][0]['token'] == False

def test_invalid_token():
    ''' test function to ensure the logout function catches invalid token error '''
    clear()
    email_test = "z5309388@unsw.edu.au"
    password_test = 'Password1'
    name_first_test = 'James'
    name_last_test = 'Turner'
    wrong_token = "abc"
    #wrong_token = encode_token("abc")
    auth_register(email_test, password_test, name_first_test, name_last_test)
    with pytest.raises(AccessError):
        assert auth_logout(wrong_token)['is_success'] == False
