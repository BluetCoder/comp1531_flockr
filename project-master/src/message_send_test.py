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

def test_message_send():
    '''testing message_send function'''
    result = setup()
    # Data['channels'][0]['messages'] = []
    message.message_send(result['token'], 1, 'Think before I act.')
    assert Data['channels'][0]['messages'][0]['message_id'] == 1
    assert Data['channels'][0]['messages'][0]['u_id'] == 1
    assert Data['channels'][0]['messages'][0]['message'] == 'Think before I act.'
    #assert Data['channels'][0]['messages'][0]['time_created'] == 1111111111

def test_message_length():
    '''if message length > 1000, raise InputError'''
    result = setup()

    string = ''
    for i in range(1001):
        string = string + str(i)

    with pytest.raises(InputError):
        assert message.message_send(result['token'],1,string)

def test_sender_membership():
    '''if sender not member of channel, raise AccessError'''
    result = setup()

    with pytest.raises(AccessError):
        assert message.message_send(result['token2'],1,'Think before I act.')

def test_return_value():
    '''test return of correct message_id'''
    result = setup()
    # Data['channels'][0]['messages'] = []
    result = message.message_send(result['token'], 1, 'Think before I act.')
    assert result == {'message_id': 1}
