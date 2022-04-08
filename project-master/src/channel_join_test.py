''' test functions to confirm the absence of bugs in channel_join function in channel.py '''

import pytest
import auth
from structure import Data
from error import InputError
from error import AccessError
from channel import channel_join
from channels import channels_create
from other import clear

#catch input error:
# - channel id is not valid
#catch access error:
# - if private channel, check if global owner. If not, not allowed in
# - user already in channel
#assert valid people have been added

# 1 - invalid channel, 2 - private channel, 3 - if the user already in channel
def test_invalid_no_channel():
    ''' tests an invalid channel id, ensures input error is raised'''
    # Clear the Data frame for black box testing
    clear()

    token1 = auth.auth_register(
        "z5309388@unsw.edu.au",
        'Password1', 'James', 'Turner')['token']
    channel_id = 1
    with pytest.raises(InputError):
        assert channel_join(token1, channel_id)

def test_invalid_private():
    ''' channel is private: ensures non-global user cannot join the private channel '''
    clear()
    token1 = auth.auth_register(
        "z5309388@unsw.edu.au",
        'Password1', 'James', 'Turner')['token']
    token2 = auth.auth_register(
        "z5309389@unsw.edu.au",
        'Password1', 'Kangnan', 'Wang')['token']
    ch_id = channels_create(token1, "James' Channel", False)
    with pytest.raises(AccessError):
        assert channel_join(token2, ch_id['channel_id'])

def test_invalid_token():
    ''' test function to ensure a user with an invalid token causes an error to be thrown '''
    clear()
    token1 = auth.auth_register(
        "z5309388@unsw.edu.au",
        'Password1', 'James', 'Turner')['token']
    token2 = auth.auth_register(
        "z5309389@unsw.edu.au",
        'Password1', 'Kangnan', 'Wang')['token']
    ch_id = channels_create(token1, "James' Channel", False)
    with pytest.raises(AccessError):
        assert channel_join(token2, ch_id['channel_id'])

def test_valid_global():
    ''' test function confirms that a global owner can be added to a private channel '''
    clear()
    # Check with Nick: need channel_create to make the creator is_global = True
    # Also shouldn't channel_create immediately append person to channel?
    # otherwise make is_public True, or make user a member and change channel.py
    token1 = auth.auth_register(
        "z5309388@unsw.edu.au",
        'Password1', 'James', 'Turner')['token']

    token2 = auth.auth_register(
        "Kangnan@unsw.edu.au",
        'Password1', 'Kangnan', 'Wang')['token']
    ch_id = channels_create(token2, "James Channel", False)
    channel_join(token1, ch_id['channel_id'])
    assert Data['channels'][0]['all_members'] == [
        {
            'u_id': 2,
            'name_first' : 'Kangnan',
            'name_last' : 'Wang'
        },
        {
            'u_id': 1,
            'name_first' : 'James',
            'name_last' : 'Turner'
        }
    ]


def test_valid():
    ''' tests valid joining of a channel '''
    # Clear the Data frame for black box testing
    clear()

    token1 = auth.auth_register(
        "z5309388@unsw.edu.au",
        'Password1', 'James', 'Turner')['token']

    token2 = auth.auth_register(
        "z5309389@unsw.edu.au",
        'Password1', 'Kangnan', 'Wang')['token']

    ch_id = channels_create(token1, "James Channel", True)
    # channel_join(token1, ch_id)
    channel_join(token2, ch_id['channel_id'])
    assert Data['channels'][0]['all_members'] == [
        {
            'u_id': 1,
            'name_first' : 'James',
            'name_last' : 'Turner'
        },
        {
            'u_id': 2,
            'name_first' : 'Kangnan',
            'name_last' : 'Wang'
        }
    ]
