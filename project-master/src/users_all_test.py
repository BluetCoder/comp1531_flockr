''' Imports '''
import pytest
from error import AccessError
from other import clear, users_all
import auth


def test_invalid_token():
    """ testing user_profile with invalid token """
    clear()
    result = auth.auth_register('test01@gmail.com', '111111', 'John', 'Smith')
    auth.auth_logout(result['token'])
    with pytest.raises(AccessError):
        assert users_all(result['token'])


def test_valid_users_all():
    ''' testing valid token with users_all '''
    clear()
    auth.auth_register('test01@gmail.com', '111111', 'Aha', 'Ahaha')
    result02 = auth.auth_register('test02@gmail.com', '123456', 'Emm', 'Emmmm')
    user = users_all(result02['token'])
    assert user['users'] == [
        {
            'u_id': 1,
            'email': 'test01@gmail.com',
            'name_first': 'Aha',
            'name_last': 'Ahaha',
            'handle_str': 'ahaahaha',
            'profile_img_url': None
        },
        {
            'u_id': 2,
            'email': 'test02@gmail.com',
            'name_first': 'Emm',
            'name_last':'Emmmm',
            'handle_str': 'emmemmmm',
            'profile_img_url': None
        }
    ]
