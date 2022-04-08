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

    token = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')['token']
    token2 = auth.auth_register('test02@gmail.com', '111111', 'Alice', 'Green')['token']
    result = channels.channels_create(token, 'sports', 'True')['channel_id']

    return {'channel_id' : result, 'token' : token, 'token2' : token2}
def test_valid_message_id():
    '''tests a valid message unpin'''
    result = setup()
    new = message.message_send(result['token'], 1, 'Virgil')
    message_id = new['message_id']
    message.message_pin(result['token'], message_id)
    message.message_unpin(result['token'], message_id)
    assert Data['channels'][0]['messages'][0]['is_pinned'] is False

def test_message_is_unpinned():
    '''tests a message is already unpinned'''
    result = setup()
    new = message.message_send(result['token'], 1, 'Virgil')
    message_id = new['message_id']
    with pytest.raises(InputError):
        assert message.message_unpin(result['token'], message_id)

#def test_invalid_message():

def test_nonmember_access_error():
    '''tests unpinning a message from a non-member'''
    result = setup()
    new = message.message_send(result['token'], 1, 'Virgil')
    message_id = new['message_id']
    with pytest.raises(AccessError):
        assert message.message_unpin(result['token2'], message_id)


def test_invalid_message_id():
    '''tests with a non-valid message_id'''
    result = setup()
    new = message.message_send(result['token'], 1, 'Virgil')
    message_id = new['message_id']
    message_id = "notamessage"
    with pytest.raises(InputError):
        assert message.message_unpin(result['token'], message_id)
