'''
Channels is a module which includes three functions for the creation and listing of channels.

Methods
-------

channels_create(token,name,is_public)
    Creates a new channel, appends it to the channels dictionary
    Returns a new channel_id

channels_listall lists all existing channels
    Returns a list of all existing channels on the system

channels_list lists all channels which the current user is a part of
    Returns a list of all channels which the current user is a part of

Auth is a module for the registration, log-in and log out for a new user.

Error is a module which specifies standard errors that the system
'''
import pytest
import channels
import auth
from error import InputError, AccessError
from other import clear

def test_invalid_channel_name():
    '''
    test for names which are way too long
    '''
    clear()
    token = auth.auth_register('noway@gmail.com', '111111', 'John', 'Smith')['token']
    with pytest.raises(InputError):
        assert channels.channels_create(token, 'thisisdefinitelymorethantwentychars', 'TRUE')


def test_createchannel():
    '''
    basic test for a working channel creation
    '''
    clear()
    token = auth.auth_register('noway@gmail.com', '111111', 'John', 'Smith')['token']
    # result stores a dictionary of the channel created
    result = channels.channels_create(token, 'among us', 'TRUE')
    assert result['channel_id'] == 1

def test_invalid_token():
    '''
    test that an invalid token will raise access error
    '''
    clear()
    token = auth.auth_register('noway@gmail.com', '111111', 'John', 'Smith')['token']
    auth.auth_logout(token)
    with pytest.raises(AccessError):
        assert channels.channels_create(token, 'among us', 'TRUE')
