""" High level support for functions """
from structure import Data
from error import InputError
import helper
import re
import urllib.request
from PIL import Image
import flask


def user_profile(token, u_id):
    """ Returns profile of user with u_id """
    helper.find_user_token(token)
    valid_u_id = False
    try:
        u_id = int(u_id)
    except Exception as e:
        raise InputError("u_id is not valid") from e
    
    for user in Data['users']:
        if user['u_id'] == u_id:
            valid_u_id = True
            profile = user.copy()
            profile.pop('password', None)
            profile.pop('token', None)
            profile.pop('is_global', None)
            break

    if valid_u_id is False:
        raise InputError("u_id is not valid")

    #return profile
    return {'user':profile}

def user_profile_setname(token, name_first, name_last):
    """ Changes first_name and last_name """
    u_id = helper.find_user_token(token)
    helper.length("name_first", name_first, 1, 50)
    helper.change_profile("name_first", name_first, token)
    helper.length("name_last", name_last, 1, 50)
    helper.change_profile("name_last", name_last, token)
    
    i = 0
    while i < len(Data['channels']):
        j = 0
        while j < len(Data['channels'][i]['all_members']):
            if Data['channels'][i]['all_members'][j]['u_id'] == u_id:
                Data['channels'][i]['all_members'][j]['name_first'] = name_first
                Data['channels'][i]['all_members'][j]['name_last'] = name_last
                break
            j += 1
        k = 0
        while k < len(Data['channels'][i]['owner_members']):
            if Data['channels'][i]['owner_members'][k]['u_id'] == u_id:
                Data['channels'][i]['owner_members'][k]['name_first'] = name_first
                Data['channels'][i]['owner_members'][k]['name_last'] = name_last
                break
            k += 1
        i = i + 1
    return {
    }

def checkemail(email):
    '''simple email check against regex, credit to geeksforgeeks.org '''
    regex =r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if not re.search(regex,email):
        return False

    return True


def user_profile_setemail(token, email):
    helper.find_user_token(token)
    if checkemail(email) is False:
        raise InputError("Email is invalid")
    helper.taken("email", email)
    helper.change_profile("email", email, token)
    return {
    }

def user_profile_sethandle(token, handle_str):
    helper.find_user_token(token)
    helper.length("handle_str", handle_str, 3, 20)
    helper.taken("handle_str", handle_str)
    helper.change_profile("handle_str", handle_str, token)
    return {
    }

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    helper.find_user_token(token)

    # Checking if url returns 200
    try:
        status_code = urllib.request.urlopen(img_url).getcode()
        if status_code != 200:
            raise InputError("HTTP status not 200")
    except Exception as e:
            raise InputError("Invalid img_url") from e

    # Fetching image via URL
    photo = helper.profile_image_path(token)
    try:
        urllib.request.urlretrieve(img_url, photo)
    except Exception as e:
            raise InputError("Invalid img_url") from e

    #Check if image is a jpg
    img = Image.open(photo)
    if img.format != 'JPEG':
        raise InputError("Image uploaded is not a JPG")

    #Cropping image
    imageObject = Image.open(photo)

    width, height = imageObject.size

    # Checks if dimensions are good
    if x_start > x_end or x_start == x_end:
        raise InputError("x_start is not within dimensions")
    if y_start > y_end or y_start == y_end:
        raise InputError("y_start is not within dimensions")
    helper.check_dimensions(width, x_start, "x_start")
    helper.check_dimensions(width, x_end, "x_end")
    helper.check_dimensions(height, y_start, "y_start")
    helper.check_dimensions(height, y_end, "y_end")

    cropped = imageObject.crop((int(x_start), int(y_start), int(x_end), int(y_end)))
    cropped.save(photo)

    # Update the profile image
    helper.change_profile("profile_img_url",flask.request.host_url + photo, token)

    return {}
