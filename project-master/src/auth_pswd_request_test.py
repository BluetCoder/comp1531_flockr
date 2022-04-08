'''testing function for auth/passwordreset/request'''

import pytest
import auth
from other import clear
from structure import Data
from error import InputError, AccessError

def test_bad_email1():
    '''wrong email type 1'''
    clear()
    auth.auth_register("james.owen.turner@gmail.com", "Password1",
                       "James", "Turner")
    with pytest.raises(InputError):
        assert auth.pwd_reset_request("james.owen.turnerr@gmail.com")

def test_bad_email2():
    '''wrong email type 2'''
    clear()
    auth.auth_register("james.owen.turner@gmail.com", "Password1",
                       "James", "Turner")
    with pytest.raises(InputError):
        assert auth.pwd_reset_request("james.owen.turner@gmailcom")

def test_valid_email():
    '''correct email'''
    clear()
    auth.auth_register("james.owen.turner@gmail.com", "Password1",
                       "James", "Turner")
    auth.pwd_reset_request("james.owen.turner@gmail.com")
    print(Data['reset_codes'])
    failedtest = True
    for code in Data['reset_codes']:
        length_code = len(code)
        email = code[8:length_code]
        print(email)
        if email == "james.owen.turner@gmail.com":
            failedtest = False
            break
    assert failedtest is False
