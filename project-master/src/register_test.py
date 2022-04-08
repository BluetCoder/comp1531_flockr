'''
high level support for functions
'''
import pytest
import jwt
import hashlib
import auth
from other import clear
from error import InputError
from structure import Data, SECRET
from helper import encode_token

def test_register():
    '''testing function for auth_register'''
    clear()

    result = auth.auth_register('test01@gmail.com','111111','John','Smith')
    assert result['u_id'] == 1
    assert result['token'] == encode_token(result['u_id'])
    assert Data['users'][0]['u_id'] == 1
    assert Data['users'][0]['email'] == 'test01@gmail.com'
    assert Data['users'][0]['name_first'] == 'John'
    assert Data['users'][0]['name_last'] == 'Smith'
    assert Data['users'][0]['handle_str'] == 'johnsmith'
    assert Data['users'][0]['password'] == hashlib.sha256('111111'.encode()).hexdigest()
    # assert Data['users'][0]['token'] == 'test01@gmail.com'
    assert Data['users'][0]['permission_id'] == 1

    auth.auth_register('test02@gmail.com','111111','JoHn','Smith')
    assert Data['users'][1]['handle_str'] == 'johnsmithnew'

    auth.auth_register('test03@gamil.com','111111','Johnnnnnnnnnnnnnnnnn','Smith')
    assert Data['users'][2]['handle_str'] == 'johnnnnnnnnnnnnnnnnn'

def test_invalid_email():
    '''testing invalid email as input'''
    clear()
    with pytest.raises(InputError):
        assert auth.auth_register('invalidemailaddress','111111','Alice','Green')

def test_used_email():
    '''testing used email as input'''
    clear()
    auth.auth_register('address@gmail.com','111111','John','Smith')
    with pytest.raises(InputError):
        assert auth.auth_register('address@gmail.com','111111','Shuwan','Guo')

def test_password():
    '''testing improper password as input'''
    clear()
    with pytest.raises(InputError):
        assert auth.auth_register('222222@gmail.com','1','Alice','Green')

def test_first_name():
    '''testing improper first name as input'''
    clear()
    with pytest.raises(InputError):
        assert auth.auth_register('333333@gmail.com','456789',
        'Aliceaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','Green')

def test_last_name():
    '''testing improper last name as input'''
    clear()
    with pytest.raises(InputError):
        assert auth.auth_register('444444@gmail.com','345678','John','')
