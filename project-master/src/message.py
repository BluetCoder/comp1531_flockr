'''
high level support for functions
'''
from structure import Data
from error import InputError, AccessError
import helper

def message_send(token, channel_id, message):
    '''
    Send a message from authorised user to the channel specified by channel_id
    '''
    
    # check whether user is authorised and get u_id from token
    u_id = helper.find_user_token(token)
    
    if len(message) > 1000:
        raise InputError("Message Too Long")

    flag = False
    try:
        channel_id = int(channel_id)
    except Exception as e:
        raise InputError("Invalid Channel ID") from e
    for member in Data['channels'][channel_id-1]['all_members']:
        if member['u_id'] == u_id:
            flag = True

    if flag is False:
        raise AccessError("Authorised User Not A Channel Member")

    # comine all message dictionaries into a list
    message_list = []
    for channel in Data['channels']:
        message_list = message_list + channel['messages']

    # get largest message_id in flockr
    max_id = 0
    for message_i in message_list:
        if message_i['message_id'] > max_id:
            max_id = message_i['message_id']

    max_id = max_id + 1
    time_created = helper.TimeDate_now()
    dictionary = {}
    dictionary['message_id'] = max_id
    dictionary['u_id'] = u_id
    dictionary['message'] = message
    dictionary['reacts'] = []
    dictionary['is_pinned'] = False
    dictionary['time_created'] = time_created
    dictionary['reacts'] = []
    dictionary['is_pinned'] = False

    Data['channels'][channel_id-1]['messages'].append(dictionary)
    return {
        'message_id': max_id
    }

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Send a message from authorised user to the channel specified by channel_id
    '''
    # check whether user is authorised and get u_id from token
    print("message_sendlater")
    u_id = helper.find_user_token(token)
    print("token checked")
    try:
        channel_id = int(channel_id)
    except Exception as e:
        raise InputError("Invalid Channel ID") from e
    helper.valid_channel(channel_id)
    print("channel_id checked")
    helper.check_membership(token, channel_id)
    print("valid member")
    if len(message) > 1000:
        raise InputError("Message Too Long")
    print("message good length")

    # check whether time_sent is a time in the past
    now = helper.TimeDate_now()
    if now > time_sent:
        raise InputError("Time is in the past")
    print("time good")
    # comine all message dictionaries into a list
    message_list = []
    for channel in Data['channels']:
        message_list = message_list + channel['messages']
    print("comine all message dictionaries into a list")
    # get largest message_id in flockr
    max_id = 0
    for message_i in message_list:
        if message_i['message_id'] > max_id:
            max_id = message_i['message_id']
    print("get largest message_id in flockr")
    max_id = max_id + 1

    dictionary = {}
    dictionary['message_id'] = max_id
    dictionary['u_id'] = u_id
    dictionary['token'] = helper.encode_token(u_id)
    dictionary['message'] = message
    dictionary['time_created'] = time_sent
    Data['channels'][channel_id-1]['messages'].append(dictionary)
    print("finished message_sendlater")
    print(Data['channels'][channel_id-1]['messages'])
    return {
        'message_id': max_id
    }

def message_remove(token, message_id):
    '''remove message with a specified message_id'''
    # check whether user is authorised and get u_id from token
    u_id = helper.find_user_token(token)

    if message_id == 0:
        raise InputError("Incorrect Message ID")

    channel_id = False
    for channel in Data['channels']:
        for message in channel['messages']:
            if message['message_id'] is message_id:
                channel_id = channel['channel_id']
                break

    if channel_id is False:
        raise InputError("Message No Longer Exists")

    if helper.check_flockr_owner(u_id) is not True:
        helper.check_channel_owner(message_id, u_id)

    Data['channels'][channel_id-1]['messages'].pop(message_id-1)

    return {
    }

def message_edit(token, message_id, message):
    '''edit a message of a specified message_id'''
    # check whether user is authorised and get u_id from token
    u_id = helper.find_user_token(token)

    if helper.check_flockr_owner(u_id) is not True:
        helper.check_channel_owner(message_id, u_id)

    for channel in Data['channels']:
        for message_i in channel['messages']:
            if message_i['message_id'] is message_id:
                if message == '':
                    message_remove(token, message_id)
                else:
                    message_i['message'] = message
                break

    return {
    }

def message_react(token, message_id, react_id):
    '''react to a message'''
    u_id = helper.find_user_token(token)

    channel_id = helper.find_channel_id(u_id)

    # if message in channel, return ranking of message, otherwise raise InputError
    ranking = helper.check_message_id(channel_id, message_id)

    if react_id != 1:
        raise InputError("Invalid React ID")

    # check if user rected or not
    helper.check_react(channel_id, message_id, u_id)
    
    for message in Data['channels'][channel_id-1]['messages']:
        if message['message_id'] == message_id:
            # get u_id of message sender
            sender_id = message['u_id']
            # if no react to message, append a react dictionary
            if len(message['reacts']) == 0:            
                dictionary = {}
                dictionary['react_id'] = 1
                dictionary['u_ids'] = []
                dictionary['u_ids'].append(u_id)
                dictionary['is_this_user_reacted'] = False
                message['reacts'].append(dictionary)
            # if message has been reacted to, append u_id to u_ids list of react dicationary
            else:
                message['reacts'][0]['u_ids'].append(u_id)
            break

    # check message sender reacted or not
    for i in Data['channels'][channel_id-1]['messages'][ranking]['reacts'][0]['u_ids']:
        if i == sender_id:  
            Data['channels'][channel_id-1]['messages'][ranking]['reacts'][0]['is_this_user_reacted'] = True 

    return {}

def message_unreact(token, message_id, react_id):
    '''unreact to a message'''
    u_id = helper.find_user_token(token)

    channel_id = helper.find_channel_id(u_id)

    # if message in channel, return ranking of message, otherwise raise InputError
    ranking = helper.check_message_id(channel_id, message_id)

    if react_id != 1:
        raise InputError("Invalid React ID")

    if len(Data['channels'][channel_id-1]['messages'][ranking]['reacts']) == 0:
        raise InputError("No Active React In Message")

    # unreact
    for message in Data['channels'][channel_id-1]['messages']:
        if message['message_id'] == message_id:
            if len(message['reacts'][0]['u_ids']) == 1:
                message['reacts'].pop()
            else:
                message['reacts'][0]['u_ids'].remove(u_id)
                if u_id == message['u_id']:
                    message['reacts'][0]['is_this_user_reacted'] = False
            break
        
    return {}

def message_pin(token, message_id):
    u_id = helper.find_user_token(token)

    # if user is not flockr owner, or channel_owner
    # raise AccessError
    try:
        message_id = int(message_id)
    except Exception as e:
        raise InputError("message_id is not a valid message") from e

    # for every channel, check messages
    # if message_id matches the input message_id
    # check if message_id is valid
    valid_message_id = False
    for channel in Data['channels']:
        for message_i in channel['messages']:
            print("message pin")
            print("message_i is" ,message_i['message_id'])
            print("message_id is ",message_id)
            if message_i['message_id'] == message_id:
                valid_message_id = True
                # checks for channel_membership
                channel_id = channel['channel_id']
                helper.check_membership(token, channel_id)
                if helper.check_flockr_owner(u_id) is not True:
                    #helper.check_channel_owner(message_id, u_id)
                    if helper.find_member(channel_id - 1, u_id, "owner_members") is False:
                        raise AccessError("You are not authorised")
                if message_i['is_pinned'] is True:
                    raise InputError("Message is already pinned")
                else:
                    message_i['is_pinned'] = True

    if valid_message_id is False: 
        raise InputError("message_id is not a valid message")
    return {
    }

def message_unpin(token, message_id):
    u_id = helper.find_user_token(token)

    # if user is not flockr owner, or channel_owner
    # raise AccessError
    try:
        message_id = int(message_id)
    except Exception as e:
        raise InputError("message_id is not a valid message") from e

    # for every channel, check messages
    # if message_id matches the input message_id
    # check if message_id is valid
    valid_message_id = False
    for channel in Data['channels']:
        for message_i in channel['messages']:
            print("message unpin")
            print("message_i is" ,message_i['message_id'])
            print("message_id is ",message_id)
            if message_i['message_id'] == message_id:
                valid_message_id = True
                # checks for channel_membership
                channel_id = channel['channel_id']
                helper.check_membership(token, channel_id)
                if helper.check_flockr_owner(u_id) is not True:
                    #helper.check_channel_owner(message_id, u_id)
                    if helper.find_member(channel_id - 1, u_id, "owner_members") is False:
                        raise AccessError("You are not authorised")
                if message_i['is_pinned'] is False:
                    raise InputError("Message is already unpinned")
                else:
                    message_i['is_pinned'] = False

    if valid_message_id is False: 
        raise InputError("message_id is not a valid message")

    return {
    }
