""" Imports """
import pytest
from channel import channel_addowner, channel_removeowner, channel_join
from channels import channels_create
from structure import Data
from error import InputError, AccessError
from other import clear
import auth

def test_empty_input():
    """ Test empty input """
    clear()
    with pytest.raises(AccessError):
        assert channel_removeowner("", None, None)

def test_wrong_channel():
    """ Test with wrong channel input """
    clear()
    register_output = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    channels_create(register_output['token'], 'ahahah', True)
    with pytest.raises(InputError):
        assert channel_removeowner(register_output['token'], 4, 2)

def test_not_owner():
    """ Test when user is not owner """
    clear()
    register_output = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    channel_id = channels_create(register_output['token'], 'ahahah', True)
    channel_join(register_output2['token'], channel_id['channel_id'])
    with pytest.raises(AccessError):
        assert channel_removeowner(register_output2['token'], 1, register_output['u_id'])

def test_not_an_owner():
    """ Test when target is not an owner """
    clear()
    register_output01 = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    channel_id = channels_create(register_output01['token'], 'Comp', True)
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    channel_join(register_output2['token'], channel_id['channel_id'])
    channel_addowner(
        register_output01['token'],
        channel_id['channel_id'],
        register_output2['u_id']
    )
    channel_removeowner(
        register_output01['token'],
        channel_id['channel_id'],
        register_output2['u_id']
    )
    with pytest.raises(InputError):
        assert channel_removeowner(
            register_output01['token'],
            channel_id['channel_id'],
            register_output2['u_id']
        )

def test_valid_ch_removeowner():
    """ Test valid input """
    clear()
    register_output01 = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    channel_id = channels_create(register_output01['token'], 'Comp', True)
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    channel_join(register_output2['token'], channel_id['channel_id'])
    channel_addowner(
        register_output01['token'],
        channel_id['channel_id'],
        register_output2['u_id']
    )
    channel_removeowner(
        register_output01['token'],
        channel_id['channel_id'],
        register_output2['u_id']
    )
    assert Data['channels'][0]['owner_members'] == [
        {
            'u_id': 1,
            'name_first': 'Shuwan',
            'name_last': 'Guo'
        }
    ]

def test_global():
    """ Test user is global """
    clear()
    register_output01 = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    register_output3 = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    channel_id = channels_create(register_output2['token'], 'Comp', True)
    channel_join(register_output3['token'], channel_id['channel_id'])
    channel_addowner(register_output01['token'], channel_id['channel_id'], register_output3['u_id'])
    channel_removeowner(
        register_output01['token'],
        channel_id['channel_id'],
        register_output3['u_id']
    )
    assert Data['channels'][0]['owner_members'] == [
        {
            'u_id': 2,
            'name_first': 'my',
            'name_last': 'whatever'
        }
    ]
