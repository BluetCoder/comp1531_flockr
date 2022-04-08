'''
high level support for functions
'''
import pytest
from channel import channel_details
from error import InputError, AccessError
import channel
import auth
from other import clear
from channels import channels_create

def test_empty_input():
    ''' Test with empty input '''
    with pytest.raises(AccessError):
        assert channel_details("", "")

def test_not_registered():
    ''' Test with invalid token '''
    with pytest.raises(AccessError):
        assert channel_details("abc", 3)

def test_wrong_channel():
    ''' Test with wrong input channel '''
    clear()
    register_output = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    channels_create(register_output['token'], 'ahaha', True)
    with pytest.raises(InputError):
        assert channel_details(register_output['token'], 5)

def test_not_in_the_channel():
    ''' Test with user not being in the channel '''
    clear()
    register_output = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    channel_id = channels_create(register_output['token'], 'ahaha', True)
    with pytest.raises(AccessError):
        assert channel_details(register_output2['token'], channel_id['channel_id'])

def test_valid_input():
    ''' Test with valid input and one member in channel '''
    clear()
    register_output = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    channel_id = channels_create(register_output['token'], 'ahahah', True)
    output = channel_details(register_output['token'], channel_id['channel_id'])
    assert output == {
        'name': 'ahahah',
        'owner_members' : [
            {
                'u_id': 1,
                'name_first' : 'my',
                'name_last' : 'ownsite'
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first' : 'my',
                'name_last' : 'ownsite'
            }
        ]
    }

def test_valid_input02():
    ''' Test with valid input and two members in a channel '''
    clear()
    register_output = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    channel_id = channels_create(register_output['token'], 'ahahah', True)
    channel.channel_invite(
        register_output['token'],
        channel_id['channel_id'],
        register_output2['u_id']
    )
    output = channel_details(register_output['token'], channel_id['channel_id'])
    assert output == {
        'name': 'ahahah',
        'owner_members' : [
            {
                'u_id': 1,
                'name_first' : 'my',
                'name_last' : 'ownsite'
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first' : 'my',
                'name_last' : 'ownsite'
            },
            {
                'u_id': 2,
                'name_first' : 'my',
                'name_last' : 'whatever'
            }
        ]
    }
