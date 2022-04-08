'''
Helper Functions
'''
import os
from datetime import datetime, timedelta
import jwt
import requests
from structure import Data, SECRET
from error import InputError, AccessError

def valid_channel(channel_id):
    '''Looks for channel. Raises when channel invalid. Returns channel address if successful'''
    try:
        channel_id = int(channel_id)
    except Exception as e:
        raise InputError("Invalid Channel ID") from e
    channel_flag = False
    i = 0
    for channel in Data['channels']: 
        if channel['channel_id'] == channel_id:
            channel_flag = True
            break
        i = i + 1
    if channel_flag is False:
        raise InputError("Invalid Channel ID")

    return i

def find_member(ch_adr, u_id, member_type):
    '''Finds user using u_id. False can be return if user not found.'''
    i = 0
    member_adr = False
    while i < len(Data['channels'][ch_adr][member_type]):
        if Data['channels'][ch_adr][member_type][i]['u_id'] == u_id:
            member_adr = i
            break
        i = i + 1
    return member_adr

def find_user_token(token):
    '''Finds user  using token. Assumes False can be return if user not found.'''
    try:
        token = str(token)
    except Exception as e:
        raise AccessError("Token invalid") from e
    valid_token = False
    for user in Data['users']:
        try:
            if user['u_id'] == int(decode_token(token)):
                if user['token'] == token:
                    valid_token = True
                    break
        except Exception as e:
            raise AccessError("Token invalid") from e
    if valid_token is False:
        raise AccessError("Token invalid")

    return decode_token(token)

def add_user_channel(u_id, channel_id, member_type):
    '''Adds a user to a channel. Can be used to add to all_members or owner_members'''

    first_name = ''
    last_name = ''
    for user in Data['users']:
        if user['u_id'] == u_id:
            first_name = user['name_first']
            last_name = user['name_last']
            break

    dictionary = dict()
    dictionary['u_id'] = u_id
    dictionary['name_first'] = first_name
    dictionary['name_last'] = last_name
    Data['channels'][channel_id][member_type].append(dictionary)

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

def taken(profile_type, new):
    """ Checks if name, email, etc is already taken. If not, sets it to the new name, email etc """
    for user in Data['users']:
        if user[profile_type] == new:
            raise InputError(profile_type + " is taken")

def length(profile_type, new, min_len, max_len):
    """ Checks if string is appropriate length. If it is, updates user. """
    if len(new) <= min_len:
        raise InputError(profile_type + " too short")
    if len(new) >= max_len:
        raise InputError(profile_type + " too long")

def change_profile(profile_type, new, token):
    ''' Changes the profile (e.g email, handle) to new '''
    for user in Data['users']:
        if user['token'] == token:
            user[profile_type] = new

def check_channel_owner(message_id, u_id):
    '''check if user is channel owner'''
    channel_id = 0
    flag = False

    for channel in Data['channels']:
        for message_i in channel['messages']:
            if message_i['message_id'] is message_id:
                if message_i['u_id'] == u_id:
                    flag = True
                channel_id = channel['channel_id']
                break

    for owner in Data['channels'][channel_id-1]['owner_members']:
        if owner['u_id'] == u_id:
            flag = True
            break

    if flag is False:
        raise AccessError("User not Channel Owner")


def check_flockr_owner(u_id):
    '''check if user is flockr owner'''
    flockr_owner = False
    for user in Data['users']:
        if user['u_id'] == u_id and user['permission_id'] == 1:
            flockr_owner = True
            break

    return flockr_owner

def encode_token(u_id):
    ''' encode u_id as jwt and returns a string token '''
    return jwt.encode({'token': u_id}, SECRET, algorithm='HS256').decode('utf-8')

def decode_token(token):
    ''' decodes the token returning u_id '''
    return jwt.decode(token, SECRET, algorithm='HS256')['token']

def flask_set_up(url):
    '''reset data, register a user and create a channel'''
    requests.delete(f"{url}/clear", json={})
    response = requests.post(f"{url}/auth/register", json={
        "email" : "test01@gmail.com",
        "password": "111111",
        "name_first":"John",
        "name_last": "Smith"
        })

    payload = response.json()
    token = payload['token']
    u_id = payload['u_id']

    response = requests.post(f"{url}/channels/create", json={
        "token": token,
        "name": "coding",
        "is_public": "True"
    })

    payload = response.json()
    channel_id = payload['channel_id']
    result = {"token": token, 'u_id': u_id, "channel_id": channel_id}
    return result

def find_channel_id(u_id):
    ''' finds channel id that a given user with u_id is in'''
    channel_id = 0
    for channel in Data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                channel_id = channel['channel_id']
    return channel_id

def check_message_id(channel_id, message_id):
    '''
    if message not in channel, raise InputError
    '''
    flag = False
    ranking = 0
    for message in Data['channels'][channel_id-1]['messages']:
        if message['message_id'] == message_id:  
            flag = True
            break
        ranking = ranking + 1
    if not flag:
        raise InputError("Message Not In Channel")
    return ranking

def check_react(channel_id, message_id, u_id):
    '''if no react in message, raise InputError'''
    flag = False
    for message in Data['channels'][channel_id-1]['messages']:
            if message['message_id'] == message_id:
                if len(message['reacts']) != 0:
                    for i in message['reacts'][0]['u_ids']:
                        if i == u_id:
                            flag = True
    if flag:
        raise InputError("User Already Reacted")

def get_reset_code(reset_code):
    ''' given user's reset_code, retrieves reset code from Data, 
    otherwise raises input error due to reset_code not in Data '''
    valid_code = False
    for code in Data['reset_codes']:
        if code == reset_code:
            valid_code = reset_code
            break
    if valid_code is False:
        raise InputError("Code is invalid, try again")
    return valid_code

def check_standup(ch_adr):
    '''Returns the time left of standup or None if no standup '''
    return Data['channels'][ch_adr]['standup']['time_finish']

def TimeDate_now():
    ''' returns now timestamp '''
    now = datetime.now()
    return now.timestamp()

def addSecs(length):
    ''' adds seconds to now timestamp '''
    now = datetime.now()
    later = now + timedelta(seconds=length)
    return later.timestamp()

def profile_image_path(token):
    ''' takes token and returns filename '''
    u_id = decode_token(token)
    filename = str(u_id) + '.jpg'
    #path = os.path.join('profile_pics/', filename)
    return filename

def check_dimensions(og_dim, crop_dim, dim_name):
    ''' checks dimensions of image'''
    if int(crop_dim) > int(og_dim) or int(crop_dim) < 0:
        raise InputError(dim_name + " is not within dimensions")
