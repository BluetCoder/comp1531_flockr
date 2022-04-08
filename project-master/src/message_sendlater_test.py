'''
high level support for functions
'''
import pytest
import auth
import channels
import message
from error import InputError, AccessError
from structure import Data
from other import clear

def setup():
    '''register two users and create a channel'''
    clear()

    token = auth.auth_register('test01@gmail.com','111111','John','Smith')['token']
    token2 = auth.auth_register('test02@gmail.com','111111','Alice','Green')['token']
    result = channels.channels_create(token,'sports','True')['channel_id']
    return {'channel_id' : result, 'token' : token, 'token2' : token2}

def test_message_sendlater():
    '''testing message_send function'''
    result = setup()
    # Data['channels'][0]['messages'] = []
    sendlater_result = message.message_sendlater(result['token'], 1, 'Think before I act.',9999999999)
    assert sendlater_result == {'message_id': 1}
    assert Data['channels'][0]['messages'][0]['message_id'] == 1
    assert Data['channels'][0]['messages'][0]['u_id'] == 1
    assert Data['channels'][0]['messages'][0]['message'] == 'Think before I act.'
    assert Data['channels'][0]['messages'][0]['time_created'] == 9999999999

def test_message_length():
    '''if message length > 1000, raise InputError'''
    result = setup()

    string = ''
    for i in range(1001):
        string = string + str(i)

    with pytest.raises(InputError):
        assert message.message_sendlater(result['token'],1,string,9999999999)

def test_time_sent():
    '''if time sent is in the past, raise InputError'''
    result = setup()
    time = 0
    with pytest.raises(InputError):
        assert message.message_sendlater(result['token'],1,'Think before I act.',time)
        
def test_sender_membership():
    '''if sender not member of channel, raise AccessError'''
    result = setup()

    with pytest.raises(AccessError):
        assert message.message_sendlater(result['token2'],1,'Think before I act.',9999999999)

def test_invalid_token():
    '''if sender not member of channel, raise AccessError'''
    result = setup()
    with pytest.raises(AccessError):
        assert message.message_sendlater("abc", result['channel_id'],'Think before I act.',9999999999)

def test_invalid_channel_id():
    '''if sender not member of channel, raise AccessError'''
    result = setup()

    with pytest.raises(InputError):
        assert message.message_sendlater(result['token'], 2,'Think before I act.',9999999999)

