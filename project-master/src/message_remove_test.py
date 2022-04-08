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

def test_message_remove():
    '''testing removing a message specified with a message_id'''
    result = setup()
    Data['channels'][0]['messages'] = []
    Data['channels'][0]['message_id'] = None
    message.message_send(result['token'],1,'Think before I act.')
    message.message_remove(result['token'], 1)
    assert len(Data['channels'][0]['messages']) == 0

def test_message_nonexistent():
    '''testing removing a message which no longer exists'''
    result = setup()
    Data['channels'][0]['messages'] = []
    Data['channels'][0]['message_id'] = None
    message.message_send(result['token'],1,'Think before I act.')
    message.message_remove(result['token'], 1)
    with pytest.raises(InputError):
        assert message.message_remove(result['token'],1)

def test_invalid_token():
    '''testing user authorised or not'''
    setup()
    with pytest.raises(AccessError):
        assert message.message_remove('test03@gmail.com',1)

def test_not_channel_owner():
    '''if user neither flockr owner nor channel owner, raise AccessError'''
    result = setup()
    Data['channels'][0]['messages'] = []
    message.message_send(result['token'],1,'Think before I act.')
    with pytest.raises(AccessError):
        assert message.message_remove(result['token2'],1)
