""" Imports """
import pytest
from standup import standup_start, standup_send
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
    result = setup()
    auth.auth_logout(result['token'])
    with pytest.raises(AccessError):
        assert standup_send(result['token'], result['channel_id'], "hello")

def test_invalid_ch_id():
    """ testing standup_start with invalid channel_id """
    result = setup()
    standup_start(result['token'], result['channel_id'], 100)
    with pytest.raises(InputError):
        assert standup_send(result['token'], 2, "hello")

def test_invalid_message_length():
    '''if message length > 1000, raise InputError'''
    result = setup()

    # Generates a message with over 1000 characters
    string = ''
    for i in range(1001):
        string = string + str(i)
    standup_start(result['token'], result['channel_id'], 100)
    with pytest.raises(InputError):
        assert standup_send(result['token'], result['channel_id'], string)

def test_invalid_no_standup():
    """ testing standup_send with no standup """
    result = setup()
    with pytest.raises(InputError):
        assert standup_send(result['token'], result['channel_id'], "hello")

def test_invalid_not_member():
    """ testing standup_send with no standup """
    result = setup()
    token = auth.auth_register('test03@gmail.com','111111','Harry','Potter')['token']
    standup_start(result['token'], result['channel_id'], 100)
    with pytest.raises(AccessError):
        assert standup_send(token, result['channel_id'], "hello")

def test_valid_standup_send():
    """ testing standup_send with no standup """
    result = setup()
    time_finish = standup_start(result['token'], result['channel_id'], 100)['time_finish']
    standup_send(result['token'], result['channel_id'], "hello")
    output = standup_send(result['member2'], result['channel_id'], "Yo")
    assert output == {}
    assert Data['channels'][0]['messages'][0]['message_id'] == 1
    assert Data['channels'][0]['messages'][0]['u_id'] == 1
    assert Data['channels'][0]['messages'][0]['message'] == 'johnsmith: hello\nalicegreen: Yo'
    assert Data['channels'][0]['messages'][0]['time_created'] == time_finish
# Need to check if my testing and function are implemented correctly

