''' Module to test search.py '''

import pytest
import auth
import channel
import channels
import message
from error import AccessError
from other import clear, search

#tests:
#   no messages
#   lots of messages
#   user leaves channel, no longer returns from that channel

def init_setup():
    ''' authorise users, create channel, add to channel '''
    clear()
    token1 = auth.auth_register(                            # Register James
        "z5309388@unsw.edu.au",
        'Password1', 'James', 'Turner')['token']
    token2 = auth.auth_register(                            # Register Kangnan
        "z5309389@unsw.edu.au",
        'Password1', 'Kangnan', 'Wang')['token']
    ch_id = channels.channels_create(token1, "James' Channel", True)['channel_id']
    channel.channel_join(token2, ch_id)
    variable_list = [token1, token2, ch_id]
    return variable_list

def message_exchange():
    ''' Simulate very real conversation between 2 real people on channel '''
    var_list = init_setup()
    token1 = var_list[0]
    token2 = var_list[1]
    ch_id = var_list[2]

    message.message_send(token1, ch_id, 'message 1')
    message.message_send(token2, ch_id, 'message 2')
    message.message_send(token2, ch_id, 'massage 3')
    message.message_send(token2, ch_id, 'message 4')
    message.message_send(token1, ch_id, 'message 5')
    message.message_send(token2, ch_id, 'massage 6')
    message.message_send(token1, ch_id, 'message 7')
    message.message_send(token2, ch_id, 'message 8')
    message.message_send(token2, ch_id, 'massage 9')
    return {'token1': token1, 'token2': token2, 'ch_id': ch_id}
    
def test_valid_messages():
    ''' search returns valid collection of messages'''
    var_list = init_setup()
    token2 = var_list[1]
    message_exchange()
    assert search(token2, 'massage')['messages'][0]['message_id'] == 9
    assert search(token2, 'massage')['messages'][1]['message_id'] == 6
    assert search(token2, 'massage')['messages'][2]['message_id'] == 3

def test_empty_messages():
    ''' messages removed, Access error raised '''
    var_list = init_setup()
    token1 = var_list[0]
    token2 = var_list[1]
    ch_id = channels.channels_create(token2, "Kangnan", True)['channel_id']
    assert search(token1, ch_id)['messages'] == []
    assert search(token2, ch_id)['messages'] == []

def test_user_left_channel():
    ''' user no longer part of that channel, no longer returns from that channel '''
    var_list = init_setup()
    token1 = var_list[0]
    ch_id = var_list[2]
    message_exchange()
    channel.channel_leave(token1, ch_id)
    with pytest.raises(AccessError):
        assert search(token1, 'message')
