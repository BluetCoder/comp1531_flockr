''' Imports '''
import helper
from error import InputError, AccessError
from structure import Data

def clear():
    ''' clears Data '''
    for x in Data:
        Data[x].clear()

    return {}

def users_all(token):
    helper.find_user_token(token)
    profile = []
    for user in Data['users']:
        new_user = user.copy()
        del new_user['password']
        del new_user['token']
        del new_user['permission_id']
        profile.append(new_user)

    return {'users': profile}

def admin_userpermission_change(token, u_id, permission_id):
    ''' function as above, in mod docstring '''

    # Ensures valid token, u_id
    token_id = helper.find_user_token(token)

    if token_id is u_id:
        raise AccessError("Can't change own permissions")

    # Access Error: given user with 'token' is not an owner (permission id != 1)
    if not helper.check_flockr_owner(token_id):
        raise AccessError("User is not an owner")

    valid_u_id = False
    for user in Data['users']:
        # Check if the given u_id is a valid user (input error)
        if user['u_id'] == u_id:
            valid_u_id = True
            # Check that permission_id (input) is valid (either 1 or 2)
            if permission_id in [1, 2]:
                # change the user's permission to given permission
                user['permission_id'] = permission_id
            else:
                raise InputError("Invalid permission id")
    if not valid_u_id:
        raise InputError("Invalid user id")
    return {}

def search(token, query_str):
    '''search function as defined in module docstring'''

    # test valid token, return u_id, raise errors
    u_id = helper.find_user_token(token)

    # Find channels the user is in, if not in any return access error?
    user_channels = []
    for channel in Data['channels']:
        for key in channel['all_members']:
            if u_id is key['u_id']:
                user_channels.append(channel['channel_id'])
    if user_channels == []:
        raise AccessError("User is not in any channels")

    # Search through all the messages in these channels, return
    # message list
    message_list = []
    for channel in Data['channels']:
        if channel['channel_id'] in user_channels:
            for message in channel['messages']:
                if query_str in message['message']:
                    add_message = message.copy()
                    #del add_message['token']
                    #del add_message['time_created']
                    message_list.append(add_message)
    
    # Reverses the messages so that it shows the messages the right way in frontend
    message_list = sorted(message_list, key=lambda i: i['time_created'])
    message_list.reverse()
    return {'messages': message_list}
