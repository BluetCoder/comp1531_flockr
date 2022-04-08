'''
Channels is a module which includes three functions for the creation and listing of channels.

Methods
-------

channels_create(token,name,is_public)

    Description:Creates a new channel, appends it to the channels dictionary
    Paramaters: token, name, is_public
    Returns: channel_id

channels_listall(token)
    Descriptions:Returns a list of all existing channels on the system
    Paramaters: token
    Returns: A list of dictionaries

channels_list lists all channels which the current user is a part of
    Description: Returns a list of all channels which the current user is a part of
    Paramaters: Tokens
    Returns: A list of dictionaries
'''
import jwt
from structure import Data, SECRET
from error import InputError, AccessError
from helper import find_user_token

def channels_list(token):
    '''
    Provide a list of all channels (and their associated details)
    that the authorised user is part of
    '''
    # using helper function, return the user_id from given token
    user_id = find_user_token(token)
    if user_id is False:
        raise AccessError("Invalid Token")
    i = 0
    # this function returns a list of dictionaries of keys channel_id and channel_name
    return_channels = []
    for _ in Data['channels']:
        j = 0
        dictionary = dict()

        for _ in Data['channels']:
            try:
                if Data['channels'][i]['all_members'][j]['u_id'] == user_id:
                    dictionary['channel_id'] = Data['channels'][i]['channel_id']
                    dictionary['name'] = Data['channels'][i]['name']
                    return_channels.append(dictionary)
            except IndexError:
                continue
            j += 1
        i += 1

    return {'channels':return_channels}

def channels_listall(token):
    '''
    lists all channels in the system
    '''
    is_valid = find_user_token(token)
    if is_valid is False:
        raise AccessError("Invalid Token")
    #initialise empty list, and loop through channels
    #adding each channel's id, and name to a dictionary
    #appending this dictionary to the list
    all_channels = []
    i = 0
    for _ in Data['channels']:
        append_channel = dict()
        append_channel['channel_id'] = Data['channels'][i]['channel_id']
        append_channel['name'] = Data['channels'][i]['name']
        all_channels.append(append_channel)
        i += 1

    return {'channels':all_channels}

def channels_create(token, name, is_public):
    '''
    creates a new channel
    '''
    # ensure token is validated
    is_valid = find_user_token(token)
    if is_valid is False:
        raise AccessError("Invalid Token")

    # name length error (more than 20 characters)
    if len(name) > 20:
        raise InputError("Name is more than 20 characters long")

    # determine new channel_id
    num_channels = len(Data['channels'])
    new_channel = num_channels + 1
    # use dict() to append a new channel
    dictionary = dict()
    dictionary['channel_id'] = new_channel
    dictionary['name'] = name
    dictionary['is_public'] = is_public
    #owner_member and all_member subsets will be the same at channel creation
    owner_member_dict = dict()

    i = 0
    for _ in Data['users']:
        if Data['users'][i]['u_id'] == is_valid:
            owner_member_dict['name_first'] = Data['users'][i]['name_first']
            owner_member_dict['name_last'] = Data['users'][i]['name_last']
            owner_member_dict['u_id'] = Data['users'][i]['u_id']
            break
        i += 1

    all_member_dict = owner_member_dict
    # append lists of dictionaries for all_members, owner_members, and messages
    dictionary['all_members'] = []
    dictionary['owner_members'] = []
    dictionary['all_members'].append(all_member_dict)
    dictionary['owner_members'].append(owner_member_dict)
    dictionary['messages'] = []
    dictionary['standup'] = {'time_finish': None, 'message_id': None}
    #append list of dictionaries to Data['channels]
    Data['channels'].append(dictionary)
    #return type ammended to the assignment spec
    print(Data)
    return {
        'channel_id': new_channel
    }
