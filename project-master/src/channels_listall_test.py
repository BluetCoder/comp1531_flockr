'''
High level function support
'''
import pytest
import channels
import auth
from error import AccessError
from other import clear
from structure import Data

def test_no_channels_created():
    '''
    No channels created
    '''
    clear()
    token = auth.auth_register('noway@gmail.com', '111111', 'John', 'Smith')['token']
    result = channels.channels_listall(token)
    assert result['channels'] == []

def test_one_channel_created():
    '''
    One channel created
    '''
    clear()
    token = auth.auth_register('noway@gmail.com', '111111', 'John', 'Smith')['token']
    channels.channels_create(token, 'among us', 'TRUE')
    result = channels.channels_listall(token)
    assert result['channels'][0]['name'] == 'among us'
    assert result['channels'][0]['channel_id'] == 1

def test_multiple_channels_created():
    '''
    Three channel created
    '''
    clear()
    token = auth.auth_register('noway@gmail.com', '111111', 'John', 'Smith')['token']
    channels.channels_create(token, 'among us', 'TRUE')
    channels.channels_create(token, 'pawg', 'TRUE')
    channels.channels_create(token, 'lfc', 'TRUE')
    result = channels.channels_listall(token)
    assert result['channels'][0]['name'] == 'among us'
    assert result['channels'][0]['channel_id'] == 1
    assert result['channels'][1]['name'] == 'pawg'
    assert result['channels'][2]['name'] == 'lfc'

def test_invalid_token():
    '''
    Tests invalid token
    '''
    clear()
    bad_token = "badtokenbad"
    print(Data['users'])
    with pytest.raises(AccessError):
        assert channels.channels_list(bad_token)
