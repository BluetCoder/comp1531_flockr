'''
high level support for auth_login, auth_logout and auth_register
'''
from structure import Data
from error import InputError, AccessError
import helper
from message import message_sendlater

def standup_start(token, channel_id, length):
    ''' Starts a standup for "length" seconds '''
    # Checks if token is valid
    helper.find_user_token(token)

    # Checks if channel_id is valid and returns array address of channel
    ch_adr = helper.valid_channel(channel_id)

    # Checking standup status
    '''
    standup_status = helper.check_standup(ch_adr)
    if standup_status is not None and standup_status < helper.TimeDate_now():
        raise InputError("Standup is currently running in this channel")
    '''
    is_active = standup_active(token, channel_id)['is_active']
    if is_active is True:
        raise InputError("Standup is currently running in this channel")
    
    time_finish = helper.addSecs(length)
    #time_finish = helper.TimeDate_now()
    #time_finish = time_finish + length
    Data['channels'][ch_adr]['standup'] = {'time_finish': time_finish, 'message_id': None}

    return {'time_finish': time_finish}

def standup_active(token, channel_id):
    ''' Checks if there is an active standup '''
    # Checks if token is valid
    helper.find_user_token(token)

    # Checks if channel_id is valid and returns array address of channel
    ch_adr = helper.valid_channel(channel_id)

    # Checking standup status
    standup_status = helper.check_standup(ch_adr)
    print("In standup active")
    print("Standup status is", standup_status)
    is_active = False
    time_finish = None
    if standup_status is not None:
        now = helper.TimeDate_now()
        if standup_status > now:
            is_active = True
            time_finish = Data['channels'][ch_adr]['standup']['time_finish']
    print("Standup status is", standup_status)
    return {'is_active': is_active, 'time_finish': time_finish}

def standup_send(token, channel_id, message):
    ''' Checks if there is an active standup '''
    # Checks if token is valid
    u_id = helper.find_user_token(token)

    # Checks if channel_id is valid and returns array address of channel
    ch_adr = helper.valid_channel(channel_id)
    
    valid_member = helper.find_member(ch_adr, u_id, 'all_members')
    if valid_member is False:
        raise AccessError("Authorised user is not a member of the channel")
    # Checking standup status
    standup_status = helper.check_standup(ch_adr)
    is_active = False
    if standup_status is not None:
        if standup_status - helper.TimeDate_now() > 0:
            is_active = True
    if is_active is False:
        raise InputError("No Standup is active in this channel")

    # Checking length of message
    if len(message) > 1000:
        raise InputError("Message Too Long")
    
    # Getting handle
    for user in Data['users']:
        if user['token'] == token:
            handle = user['handle_str']
            break
    message = handle + ": " + message
    # Send the message through message send_later
    message_id = Data['channels'][ch_adr]['standup']['message_id']
    print("Message send_later")
    print("message is " ,message)
    if message_id == None:
        message_id = message_sendlater(token, channel_id, message, standup_status)['message_id']
        Data['channels'][ch_adr]['standup']['message_id'] = message_id
    # If there is message already in a queue, we just add the new message by editing the old message
    else:
        for channel in Data['channels'][ch_adr]['messages']:
            if channel['message_id'] is message_id:
                old_message = channel['message'] + '\n'
                print("old message is " ,old_message)
                message_standup = old_message + message
                print("message_standup is " ,message_standup)
                channel['message'] = message_standup
    return {}
