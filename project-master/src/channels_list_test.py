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
from error import AccessError
from other import clear
from structure import Data

def test_no_channels_created():
    '''
    Tests
    '''
    clear()
    token = auth.auth_register('noway@gmail.com', '111111', 'John', 'Smith')['token']
    print(Data['users'])
    result = channels.channels_list(token)
    assert result['channels'] == []

def test_one_channel_created_by_user():
    '''
    Tests
    '''
    clear()
    token = auth.auth_register('noway@gmail.com', '111111', 'John', 'Smith')['token']
    channels.channels_create(token, 'among us', True)
    result = channels.channels_list(token)
    assert result['channels'][0]['name'] == 'among us'
    assert result['channels'][0]['channel_id'] == 1

def test_multiple_channels_created():
    '''
    Tests
    '''
    clear()
    token1 = auth.auth_register('noway@gmail.com', '111111', 'John', 'Smith')['token']
    token2 = auth.auth_register('lfc@gmail.com', '111111', 'Jordan', 'Henderson')['token']
    channels.channels_create(token1, 'among us', True)
    channels.channels_create(token2, 'lfc', True)
    channels.channels_create(token1, 'pawg', True)
    result = channels.channels_list(token1)
    assert result['channels'][0]['name'] == 'among us'
    assert result['channels'][0]['channel_id'] == 1
    assert result['channels'][1]['name'] == 'pawg'

def test_invalid_token():
    '''
    Tests
    '''
    clear()
    bad_token = "badtokenbad"
    print(Data['users'])
    with pytest.raises(AccessError):
        assert channels.channels_list(bad_token)
