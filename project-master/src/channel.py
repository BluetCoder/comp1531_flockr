'''
high level support for functions
'''
from structure import Data
from error import InputError, AccessError
import helper

def check_channel(channel_id):
    '''check validity of channel'''
    if channel_id > len(Data['channels']):
        raise InputError("Invalid Channel ID")

def check_user(u_id):
    '''check validity of user'''
    if u_id > len(Data['users']):
        raise InputError("Invalid User ID")

def check_member(channel_id, u_id):
    '''check membership'''
    length = int(channel_id) - 1

    for member in Data['channels'][length]['all_members']:
        if member['u_id'] == u_id:
            raise AccessError("Already Member")

def channel_invite(token, channel_id, u_id):
    '''invite a user to channel'''
    is_valid = helper.find_user_token(token)
    if is_valid is False:
        raise AccessError("Invalid Token")
    check_channel(channel_id)

    check_user(u_id)

    check_member(channel_id, u_id)

    flag = False

    for user in Data['users']:
        if user['token'] == token:
            flag = user['u_id']

    if flag is False:
        raise AccessError("Token is invalid")

    all_member_dict = dict()

    i = 0
    for user in Data['users']:
        if Data['users'][i]['u_id'] == u_id:
            all_member_dict['name_first'] = Data['users'][i]['name_first']
            all_member_dict['name_last'] = Data['users'][i]['name_last']
            all_member_dict['u_id'] = u_id
            # all_member_dict['token'] = Data['users'][i]['token']
            break
        i += 1

    length = int(channel_id) - 1
    Data['channels'][length]['all_members'].append(all_member_dict)

    return {
    }

def channel_details(token, channel_id):
    '''get channel detail'''
    # find the uid with token
    u_id = helper.find_user_token(token)

    # Looks for the channel
    ch_adr = helper.valid_channel(channel_id)
    user_member = helper.find_member(ch_adr, u_id, "all_members")
    if user_member is False:
        raise AccessError("Authorised user is not a member of the channel")
    detail = Data['channels'][ch_adr].copy()
    detail.pop('channel_id', None)
    detail.pop('is_public', None)
    detail.pop('messages', None)
    detail.pop('standup', None)
    return detail


def check_membership(token, channel_id):
    '''check membership'''
    for user in Data['users']:
        if user['token'] == token:
            u_id = user['u_id']
    flag = False
    for member in Data['channels'][channel_id-1]['all_members']:
        if member['u_id'] == u_id:
            flag = True

    if flag is False:
        raise AccessError("Authorised User Not A Channel Member")

def channel_messages(token, channel_id, start):
    '''return at most 50 messages from start'''
    #is_valid = helper.find_user_token(token)
    #if is_valid is False:
    #    raise AccessError("Invalid Token")
    
    helper.find_user_token(token)
    #if u_id is False:
    #    raise AccessError("Token is invalid")

    try:
        channel_id = int(channel_id)
    except Exception as e:
        raise InputError("Invalid Channel ID") from e

    try:
        channel_id = int(channel_id)
    except:
        raise InputError("Invalid Channel ID")
    if len(Data['channels']) < channel_id:
        raise InputError("Invalid Channel")

    length = len(Data['channels'][channel_id-1]['messages'])
    check_membership(token, channel_id)
    try:
        start = int(start)
    except Exception as e:
        raise InputError("Invalid start") from e
    

    dictionary = dict()
    
    if length == 0:
        dictionary['messages'] = []
        dictionary['start'] = start
        dictionary['end'] = -1
        return dictionary
        #return {}
    if start > (length-1):
        raise InputError("Messages Not Found")
    messages = Data['channels'][channel_id-1]['messages'][start:start+50].copy()

    # Reverses the messages so that it shows the messages the right way in frontend
    messages = sorted(messages, key=lambda i: i['time_created'])
    messages.reverse()

    # Deletes messages that have time_created after time now
    now = helper.TimeDate_now()
    for message in messages:
        if message['time_created'] > now:
            messages.remove(message)

    dictionary['messages'] = messages
    dictionary['start'] = start
    dictionary['end'] = start+50
    
    
    if len(Data['channels'][channel_id-1]['messages']) <= 50:
        dictionary['end'] = -1

    return dictionary

def channel_leave(token, channel_id):
    '''leave a channel'''
    u_id = helper.find_user_token(token)
    if u_id is False:
        raise AccessError("Invalid Token")

    ch_adr = helper.valid_channel(channel_id)

    member_adr = helper.find_member(ch_adr, u_id, 'all_members')
    if member_adr is False:
        raise AccessError("Authorised user is not a member of the channel")

    del Data['channels'][ch_adr]['all_members'][member_adr]

    member_adr = helper.find_member(ch_adr, u_id, 'owner_members')

    if member_adr is not False:
        del Data['channels'][ch_adr]['owner_members'][member_adr]
    return {
    }

def channel_join(token, channel_id):
    '''join a channel'''
    # Find user, save u_id, first_name, last_name, check if global owner or not
    u_id = helper.find_user_token(token)
    is_global = helper.check_flockr_owner(u_id)
    ch_adr = helper.valid_channel(channel_id)

    # Test for public channel
    if Data['channels'][ch_adr]['is_public'] is False and is_global is False:
        raise AccessError("Private channel")

    target_flag = helper.find_member(ch_adr, u_id, 'all_members')
    if target_flag is not False:
        raise InputError("User is already in the channel")

    helper.add_user_channel(u_id, ch_adr, "all_members")
    return {}

def channel_addowner(token, channel_id, u_id):
    '''add owner of channel'''
    owner_id = helper.find_user_token(token)
    is_global = helper.check_flockr_owner(owner_id)
    # is_global = helper.valid_global(token)
    if is_global is False:
        ch_adr = helper.valid_channel(channel_id)
        owner_flag = helper.find_member(ch_adr, owner_id, 'owner_members')
        if owner_flag is False:
            raise AccessError("You cannot add owner")
    else:
        ch_adr = helper.valid_channel(channel_id)

    target_flag = helper.find_member(ch_adr, u_id, 'all_members')
    if target_flag is False:
        raise InputError("User Not Member Of Channel")
    target_flag = helper.find_member(ch_adr, u_id, 'owner_members')
    if target_flag is not False:
        raise InputError("The user is already an owner")

    helper.add_user_channel(u_id, ch_adr, "owner_members")
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    '''remove owner of channel'''
    # is_global = helper.valid_global(token)
    owner_id = helper.find_user_token(token)
    is_global = helper.check_flockr_owner(owner_id)
    if is_global is False:
        ch_adr = helper.valid_channel(channel_id)
        owner_flag = helper.find_member(ch_adr, owner_id, 'owner_members')
        if owner_flag is False:
            raise AccessError("You cannot remove owner")
    else:
        ch_adr = helper.valid_channel(channel_id)
    member_adr = helper.find_member(ch_adr, u_id, 'owner_members')
    if member_adr is False:
        raise InputError("The user is not an owner")
    del Data['channels'][ch_adr]['owner_members'][member_adr]
    return {
    }
