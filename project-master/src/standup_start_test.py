""" Imports """
import pytest
from standup import standup_start
from error import InputError, AccessError
from other import clear
from structure import Data
import auth
import channels
import channel

def setup():
    '''register two users and create a channel. Both users in the channel'''
    clear()
    token = auth.auth_register('test01@gmail.com','111111','John','Smith')['token']
    token2 = auth.auth_register('test02@gmail.com','111111','Alice','Green')['token']
    result = channels.channels_create(token,'sports','True')['channel_id']
    channel.channel_join(token2, result)
    return {'channel_id' : result, 'token' : token, 'member2' : token2}

def test_invalid_token():
    """ testing standup_start with invalid token """
    clear()
    token = auth.auth_register('test01@gmail.com','111111','John','Smith')['token']
    auth.auth_logout(token)
    with pytest.raises(AccessError):
        assert standup_start(token, 1, 1)

def test_invalid_ch_id():
    """ testing standup_start with invalid channel_id """
    result = setup()
    with pytest.raises(InputError):
        assert standup_start(result['token'], 2, 10)

def test_valid_standup_start():
    """ testing standup_start with valid inputs """
    result = setup()
    output = standup_start(result['token'], result['channel_id'], 100)
    assert Data['channels'][0]['standup']['time_finish'] == output['time_finish']

def test_invalid_active_standup():
    """ testing standup_start with invalid channel_id """
    result = setup()
    standup_start(result['token'], result['channel_id'], 100)
    with pytest.raises(InputError):
        assert standup_start(result['token'], 2, 10)
# Need to check if my testing and function are implemented correctly
