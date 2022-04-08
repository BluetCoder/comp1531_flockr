''' test functions for admin user permission change '''

import pytest
import auth
import helper
from error import InputError, AccessError
from structure import Data
from other import clear, admin_userpermission_change

# Tests
#   valid permission change
#   token is not an owner
#   changing own permission
#   u_id is not valid user
#   permission_id is not 1,2

def init_setup():
    ''' authorise users, create channel, add to channel '''
    clear()
    token1 = auth.auth_register(                            # Register James
        "z5309388@unsw.edu.au",
        'Password1', 'James', 'Turner')['token']
    token2 = auth.auth_register(                            # Register Kangnan
        "z5309389@unsw.edu.au",
        'Password1', 'Kangnan', 'Wang')['token']
    variable_list = [token1, token2]
    return variable_list

def test_valid():
    ''' valid permission change '''
    var_list = init_setup()
    token1 = var_list[0]
    token2 = var_list[1]
    token2_id = helper.find_user_token(token2)
    admin_userpermission_change(token1, token2_id, 1)
    for user in Data['users']:
        if user['token'] is token2:
            assert user['permission_id'] == 1
            break

def test_not_owner():
    ''' given token doesn't refer to owner, can't change permissions '''
    var_list = init_setup()
    token1 = var_list[0]
    token2 = var_list[1]
    token1_id = helper.find_user_token(token1)
    with pytest.raises(AccessError):
        assert admin_userpermission_change(token2, token1_id, 1)

def test_own_permission():
    ''' user can't change own permissions'''
    var_list = init_setup()
    token1 = var_list[0]
    token1_id = helper.find_user_token(token1)
    with pytest.raises(AccessError):
        assert admin_userpermission_change(token1, token1_id, 1)

def test_uid_invalid():
    ''' u_id refers to invalid user '''
    var_list = init_setup()
    token1 = var_list[0]
    with pytest.raises(InputError):
        assert admin_userpermission_change(token1, 69, 1)

def test_invalid_perm_id():
    ''' permission id is not 1 or 2 '''
    var_list = init_setup()
    token1 = var_list[0]
    token2 = var_list[1]
    token2_id = helper.find_user_token(token2)
    with pytest.raises(InputError):
        assert admin_userpermission_change(token1, token2_id, 3)
    
