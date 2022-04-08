'''
high level support for auth_login, auth_logout and auth_register
'''
import re
import hashlib
import random
import string
import yagmail
import jwt
from structure import Data, SECRET
from error import InputError, AccessError
import helper


def auth_login(email, password):
    '''log user in via email and password'''
    if re.search('@', email) is None:
        raise InputError("Invalid Email Address")

    member = False
    valid_password = False

    for user in Data['users']:
        if user['email'] == email:
            member = True
            if user['password'] == hashlib.sha256(password.encode()).hexdigest():
                valid_password = True
                u_id = user['u_id']
                #token == user['email']
                user['token'] = helper.encode_token(u_id)
                # user['is_success'] = False
                break

    if member is False:
        raise InputError("Email used is not registered")

    if valid_password is False:
        raise InputError("Password is not correct")

    return {
        'u_id': u_id,
        'token': helper.encode_token(u_id)
    }

def auth_logout(token):
    '''log user out with token'''
    is_success = False
    is_valid = helper.find_user_token(token)
    if is_valid is False:
        raise AccessError("Invalid Token")

    for user in Data['users']:
        if user['u_id'] == helper.decode_token(token):
            user['token'] = False
            is_success = True
            break

    return {'is_success': is_success}


def check_email(email):
    '''check whether email is valid or not'''
    if re.search('@', email) is None:
        raise InputError("Invalid Email Address")

    for user in Data['users']:
        if user['email'] == email:
            raise InputError("Email Address Already Used By Another User")

def handle_convert(name_first, name_last):
    '''create a handle'''
    handle = name_first + name_last
    handle = handle.lower()

    if len(handle) > 20:
        slice_object = slice(20)
        handle = handle[slice_object]

    for user in Data['users']:
        if user['handle_str'] == handle:
            handle = handle + 'new'
            break

    return handle

def auth_register(email, password, name_first, name_last):
    '''register a user'''
    check_email(email)

    if len(password) < 6:
        raise InputError("Password Less Than 6 Characters Long")

    if (len(name_first) < 1) | (len(name_first) > 50):
        raise InputError("First Name Characters Not Between 1 and 50")

    if (len(name_last) < 1) | (len(name_last) > 50):
        raise InputError("Last Name Characters Not Between 1 and 50")

    dictionary = dict()

    length = len(Data['users']) + 1

    handle = handle_convert(name_first, name_last)
    password = hashlib.sha256(password.encode()).hexdigest()
    dictionary['u_id'] = length
    dictionary['email'] = email
    dictionary['name_first'] = name_first
    dictionary['name_last'] = name_last
    dictionary['handle_str'] = handle
    dictionary['password'] = password
    dictionary['token'] = helper.encode_token(length)
    dictionary['profile_img_url'] = None

    if length == 1:
        dictionary['permission_id'] = 1
    else:
        dictionary['permission_id'] = 2

    Data['users'].append(dictionary)

    return {
        'u_id': length,
        'token': helper.encode_token(length)
    }

def pwd_reset_request(email):
    ''' send request for code to reset password '''
    valid_email = False
    for user in Data['users']:
        if user['email'] == email:
            valid_email = True
            break
    if valid_email is False:
        raise InputError("Email invalid")

    #Following 3 lines sourced from https://pynative.com/python-generate-random-string/
    length = 8
    letters_and_digits = string.ascii_letters + string.digits
    reset_code = ''.join((random.choice(letters_and_digits) for i in range(length)))

    reset_code = reset_code + email
    #store code in Data temporarily
    Data['reset_codes'] = []
    Data['reset_codes'].append(reset_code)

    #initializing the server connection
    yag = yagmail.SMTP(user='flockruser69@gmail.com', password='P4ssword69')

    #sending the email
    yag.send(to=email, subject="Password reset request",
             contents="You recently requested to change your password. " +
             "Your unique code is: %s ." % reset_code)
             #"If you did make this request, please change your password immediately." % reset_code

def pwd_reset_reset(reset_code, new_password):
    ''' given reset_code and new_password, attempts to reset user's password'''

    # check for invalid code
    helper.get_reset_code(reset_code)

    #check for invalid new_password
    if len(new_password) < 6:
        raise InputError("Password Less Than 6 Characters Long")

    # extract email from code
    length_code = len(reset_code)
    email = reset_code[8:length_code]
    for user in Data['users']:
        if user['email'] == email:
            user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
            break

    # remove code in Data once change pswd successful
    for code in Data['reset_codes']:
        if code is reset_code:
            del code
            break
