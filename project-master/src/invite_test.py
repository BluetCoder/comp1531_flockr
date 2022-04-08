'''
high level support for functions
'''
import pytest
import auth
import channel
import channels
from error import InputError, AccessError
from structure import Data
from other import clear

def setup():
    '''register two users and create a channel'''
    clear()

    token = auth.auth_register('test01@gmail.com','111111','John','Smith')['token']
    auth.auth_register('test02@gmail.com','111111','Alice','Green')
    channels.channels_create(token,'sports','True')
    return token

def test_invite():
    '''test channel_invite'''
    token = setup()

    channel.channel_invite(token,1,2)

    assert len(Data['channels'][0]['all_members']) == 2
    assert Data['channels'][0]['all_members'][1]['u_id'] == 2
    assert Data['channels'][0]['all_members'][1]['name_first'] == 'Alice'
    assert Data['channels'][0]['all_members'][1]['name_last'] == 'Green'
    #assert Data['channels'][0]['all_members'][1]['token'] == 'test02@gmail.com'

def test_invalid_channel():
    '''test invalid channel as input of channel_invite function'''
    token = setup()
    with pytest.raises(InputError):
        assert channel.channel_invite(token,9,2)

def test_invalid_user():
    '''test invalid user as input of channel_invite function'''
    token = setup()
    with pytest.raises(InputError):
        assert channel.channel_invite(token,1,10)

def test_user_member():
    '''test inviting a user who is already a member of the channel'''
    token = setup()
    channel.channel_invite(token,1,2)
    with pytest.raises(AccessError):
        assert channel.channel_invite(token,1,2)

def test_inviter():
    '''test inviter who is not a channel member as input of channel_invite function'''
    token = setup()
    with pytest.raises(AccessError):
        assert channel.channel_invite(token,1,1)

def test_invalid_token():
    '''test token validity'''
    setup()
    with pytest.raises(AccessError):
        assert channel.channel_invite('abc',1,1)
