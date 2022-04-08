""" Imports """
import pytest
from channel import channel_addowner, channel_join
from channels import channels_create
from structure import Data
from error import InputError, AccessError
from other import clear
import auth

def setup():
    """ Setup Data """
    clear()
    token = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')['token']
    auth.auth_register('test02@gmail.com', '111111', 'Alice', 'Green')
    channels_create(token, 'sports', 'True')

def test_empty_input():
    """ Test empty input """
    setup()
    with pytest.raises(AccessError):
        assert channel_addowner("", None, None)

def test_wrong_channel():
    """ Test with wrong channel input """
    clear()
    register_output = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    channels_create(register_output['token'], 'ahahah', True)
    with pytest.raises(InputError):
        assert channel_addowner(register_output['token'], 4, 2)

def test_not_owner():
    """ Test when user is not owner """
    clear()
    register_output = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    channel_id = channels_create(register_output['token'], 'ahahah', True)
    channel_join(register_output2['token'], channel_id['channel_id'])
    with pytest.raises(AccessError):
        assert channel_addowner(register_output2['token'], 1, 2)

def test_logged_out():
    """ Test when user is logged out """
    clear()
    register_output01 = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    channel_id = channels_create(register_output01['token'], 'Comp', True)
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    auth.auth_logout(register_output01['token'])
    channel_join(register_output2['token'], channel_id['channel_id'])
    with pytest.raises(AccessError):
        assert channel_addowner(
            register_output01['token'],
            channel_id['channel_id'],
            register_output2['u_id']
        )

def test_valid_ch_addowner():
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
    assert Data['channels'][0]['owner_members'] == [
        {
            'u_id': 1,
            'name_first': 'Shuwan',
            'name_last': 'Guo'
        },
        {
            'u_id': 2,
            'name_first': 'my',
            'name_last': 'whatever'
        }
    ]

def test_already_owner():
    """ Test when member being made owner is already an owner """
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
    with pytest.raises(InputError):
        assert channel_addowner(
            register_output01['token'],
            channel_id['channel_id'],
            register_output2['u_id']
        )

def test_not_member():
    """ Test when member being made owner is not a member """
    clear()
    register_output01 = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    channel_id = channels_create(register_output01['token'], 'Comp', True)
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    with pytest.raises(InputError):
        assert channel_addowner(
            register_output01['token'],
            channel_id['channel_id'],
            register_output2['u_id']
        )

def test_global():
    """ Test user is global """
    clear()
    register_output01 = auth.auth_register('susanshuwanguo@gmail.com', '123456', 'Shuwan', 'Guo')
    register_output2 = auth.auth_register('my.whatever@ourearth.org', '123456', 'my', 'whatever')
    register_output3 = auth.auth_register('my.ownsite@ourearth.org', '111111', 'my', 'ownsite')
    channel_id = channels_create(register_output2['token'], 'Comp', True)
    channel_join(register_output3['token'], channel_id['channel_id'])
    channel_addowner(register_output01['token'], channel_id['channel_id'], register_output3['u_id'])
    assert Data['channels'][0]['owner_members'] == [
        {
            'u_id': 2,
            'name_first': 'my',
            'name_last': 'whatever'
        },
        {
            'u_id': 3,
            'name_first': 'my',
            'name_last': 'ownsite'
        }
    ]
