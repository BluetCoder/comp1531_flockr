'''
high level support for functions
'''
import pytest
import auth
import channels
import message
from error import AccessError
from structure import Data
from other import clear

def setup():
    '''register two users and create a channel'''
    clear()

    token = auth.auth_register('test01@gmail.com','111111','John','Smith')['token']
    token2 = auth.auth_register('test02@gmail.com','111111','Alice','Green')['token']
    result = channels.channels_create(token,'sports','True')['channel_id']
    return {'channel_id' : result, 'token' : token, 'token2' : token2}

def test_message_edit():
    '''testing editing a message with a specified message_id'''
    result = setup()
    Data['channels'][0]['messages'] = []
    message.message_send(result['token'],1,'Think before I act.')
    message.message_edit(result['token'], 1, 'No pain, no gain')
    assert Data['channels'][0]['messages'][0]['message'] == 'No pain, no gain'

def test_empty_input():
    '''if new text is an empty string, message deleted'''
    result = setup()
    Data['channels'][0]['messages'] = []
    message.message_send(result['token'],1,'Think before I act.')
    message.message_edit(result['token'], 1, '')
    assert len(Data['channels'][0]['messages']) == 0

def test_invalid_token():
    '''testing user authorised or not'''
    setup()
    with pytest.raises(AccessError):
        assert message.message_edit('test03@gmail.com',1,'Think before I act.')

def test_not_channel_owner():
    '''if user neither flockr owner nor channel owner, raise AccessError'''
    result = setup()
    Data['channels'][0]['messages'] = []
    with pytest.raises(AccessError):
        assert message.message_edit(result['token2'],1,'Think before I act.')
