''' testing auth.pwd_reset_reset() '''
import hashlib
import pytest
from other import clear
from structure import Data
import auth
from error import InputError, AccessError

def test_invalid_code():
    ''' code is not in Database '''
    clear()
    auth.auth_register("james.owen.turner@gmail.com", "Password1",
                       "James", "Turner")
    auth.pwd_reset_request("james.owen.turner@gmail.com")
    with pytest.raises(InputError):
        assert auth.pwd_reset_reset("CdkJbHc69", "Password2")

def test_invalid_pwd():
    ''' password too short '''
    clear()
    auth.auth_register("james.owen.turner@gmail.com", "Password1",
                       "James", "Turner")
    auth.pwd_reset_request("james.owen.turner@gmail.com")
    reset_code = Data['reset_codes'][0]
    with pytest.raises(InputError):
        assert auth.pwd_reset_reset(reset_code, "Pass2")

def test_valid():
    ''' valid request and reset process '''
    clear()
    auth.auth_register("james.owen.turner@gmail.com", "Password1",
                       "James", "Turner")              
    auth.pwd_reset_request("james.owen.turner@gmail.com")
    reset_code = Data['reset_codes'][0]
    auth.pwd_reset_reset(reset_code, "Password2")
    assert Data['users'][0]['password'] == hashlib.sha256('Password2'.encode()).hexdigest()
