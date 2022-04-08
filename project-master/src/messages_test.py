'''
high level support for functions
'''
import pytest
import auth
import channel
import channels
from error import InputError, AccessError
from structure import Data
from other import clear
import message

def message_generate(token, channel_id, length):
    '''generate messages in channel'''
    for i in range(length):
        message.message_send(token, channel_id, 'Think before I act.')
        i = i + 1

def setup():
    '''register two users and create a channel'''
    clear()

    token = auth.auth_register('test01@gmail.com','111111','John','Smith')['token']
    token2 = auth.auth_register('test02@gmail.com','111111','Alice','Green')['token']
    result = channels.channels_create(token,'sports','True')['channel_id']
    return {'channel_id' : result, 'token' : token, 'non_member' : token2}

def test_messages():
    '''testing channel_messages function'''
    result_1 = setup()
    channel_id = result_1['channel_id']
    assert channel_id == 1
    message_generate(result_1['token'], channel_id, 51)
    result_3 = channel.channel_messages(result_1['token'], 1, 0)
    assert result_3['start'] == 0
    assert result_3['end'] == 50
    result_4 = channel.channel_messages(result_1['token'],1,25)
    assert result_4['start'] == 25
    assert result_4['end'] == 75

def test_invalid_channel():
    ''' testing invalid channel as input of channel_messages function '''
    token = setup()['token']
    with pytest.raises(InputError):
        assert channel.channel_messages(token,3,2)

def test_start():
    ''' testing improper start number '''
    token = setup()['token']
    message_generate(token, 1, 1)
    with pytest.raises(InputError):
        assert channel.channel_messages(token,1,60)

def test_member():
    ''' testing non-member as input of channel_messages function '''
    result = setup()
    message_generate(result['token'], 1, 3)
    with pytest.raises(AccessError):
        assert channel.channel_messages(result['non_member'], 1, 2)

def test_token():
    ''' testing token validity '''
    setup()
    with pytest.raises(AccessError):
        assert channel.channel_messages('1',1,2)

def test_end_value():
    ''' testing end == -1 when least recent message is returned '''
    result_1 = setup()
    channel_id = result_1['channel_id']
    message_generate(result_1['token'], channel_id, 50)
    result_3 = channel.channel_messages(result_1['token'], 1, 0)
    assert result_3['start'] == 0
    assert result_3['end'] == -1

def test_length_0():
    ''' test no messages '''
    result_1 = setup()
    result_2 = channel.channel_messages(result_1['token'], 1, 0)
    assert result_2 == {'end':-1,'messages':[],'start':0}
