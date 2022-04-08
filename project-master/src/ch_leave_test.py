""" Imports """
import pytest
from channel import channel_leave, channel_join
from structure import Data
from error import InputError, AccessError
from channels import channels_create
import auth
from other import clear

def test_empty_input():
    """ Test empty input """
    clear()
    with pytest.raises(AccessError):
        assert channel_leave("", "")

def test_wrong_channel():
    """ Test wrong channel """
    clear()
    register_output02 = auth.auth_register('henry.zhang@gmail.com', '345678', 'Henry', 'Zhang')
    channels_create(register_output02['token'], 'Comp', True)
    with pytest.raises(InputError):
        assert channel_leave(register_output02['token'], 4)

def test_not_member():
    """ Test input is not a member """
    clear()
    register_output01 = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    register_output02 = auth.auth_register('henry.zhang@gmail.com', '345678', 'Henry', 'Zhang')
    channel_id = channels_create(register_output02['token'], 'Comp', True)
    with pytest.raises(AccessError):
        assert channel_leave(register_output01['token'], channel_id['channel_id'])

def test_logged_out():
    """ Test when user is logged out """
    clear()
    register_output01 = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    channel_id = channels_create(register_output01['token'], 'Comp', False)
    auth.auth_logout(register_output01['token'])
    with pytest.raises(AccessError):
        assert channel_leave(register_output01['token'], channel_id['channel_id'])

def test_valid_ch_leave():
    """ Testing valid inputs """
    clear()
    token1 = auth.auth_register(
        "z5309388@unsw.edu.au",
        'Password1', 'James', 'Turner')['token']
    token2 = auth.auth_register(
        "z5309389@unsw.edu.au",
        'Password1', 'Kangnan', 'Wang')['token']
    ch_id = channels_create(token1, "James Channel", True)
    channel_join(token2, ch_id['channel_id'])
    channel_leave(token2, ch_id['channel_id'])
    assert Data['channels'][0]['all_members'] == [
        {
            'u_id': 1,
            'name_first' : 'James',
            'name_last' : 'Turner'
        }
    ]

def test_valid_ch_leave01():
    """ Testing valid inputs again """
    clear()
    token1 = auth.auth_register(
        "z5309388@unsw.edu.au",
        'Password1', 'James', 'Turner')['token']
    token2 = auth.auth_register(
        "z5309389@unsw.edu.au",
        'Password1', 'Kangnan', 'Wang')['token']
    ch_id = channels_create(token1, "James Channel", True)
    channel_join(token2, ch_id['channel_id'])
    channel_leave(token2, ch_id['channel_id'])
    assert Data['channels'][0]['all_members'] == [
        {
            'u_id': 1,
            'name_first' : 'James',
            'name_last' : 'Turner'
        }
    ]
    ch_id = channels_create(token2, "Kangnan Channel", True)
    channel_leave(token2, ch_id['channel_id'])
    assert Data['channels'][1]['all_members'] == []
    assert Data['channels'][1]['owner_members'] == []
