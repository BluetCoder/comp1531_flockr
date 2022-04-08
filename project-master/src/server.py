'''
high level support for functions
'''
from json import dumps
from flask_cors import CORS
from flask import Flask, request, send_from_directory
import channel
import channels
import auth
import message
import other
from error import InputError
import user
import standup
import helper
from structure import Data

def defaultHandler(err):
    '''
    default handling of error
    '''
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


@APP.route('/<path:filename>')
def send_js(filename):
    return send_from_directory('', filename)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    ''' echo example'''
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/login", methods=['POST'])
def login():
    '''auth/login route'''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    return dumps(auth.auth_login(email, password))

@APP.route("/auth/logout", methods=['POST'])
def logout():
    '''auth/logout route'''
    payload = request.get_json()
    token = payload['token']
    return dumps(auth.auth_logout(token))

@APP.route("/auth/register", methods=['POST'])
def register():
    '''
    register user
    '''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
    return dumps(auth.auth_register(email, password, name_first, name_last))

@APP.route("/channels/create", methods=['POST'])
def channels_create():
    '''channels_create route'''
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    return dumps(channels.channels_create(token,name,is_public))


@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    '''channels_listall route'''
    token = request.args.get('token')
    return dumps(channels.channels_listall(token))

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    '''channels_list route'''
    token = request.args.get('token')
    return dumps(channels.channels_list(token))


@APP.route("/clear", methods=['DELETE'])
def clear():
    '''
    reset Data structure to be empty
    '''
    return dumps(other.clear())

@APP.route("/users/all", methods=['GET'])
def users_all():
    '''show list of users'''
    token = request.args.get('token')
    return dumps(other.users_all(token))

@APP.route("/admin/userpermission/change", methods=['POST'])
def admin_userpermission_change():
    '''Changes admin permission '''
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    return dumps(other.admin_userpermission_change(token, u_id, permission_id))
    
@APP.route("/search", methods=['GET'])
def search():
    ''' Search route'''
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(other.search(token, query_str))

@APP.route("/user/profile", methods=['GET'])
def user_profile():
    '''show user profile'''
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return dumps(user.user_profile(token, u_id))

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname():
    '''update user name'''
    payload = request.get_json()
    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']
    return dumps(user.user_profile_setname(token, name_first, name_last))

@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
    payload = request.get_json()
    token = payload['token']
    email = payload['email']
    return dumps(user.user_profile_setemail(token, email))
    
@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle():
    payload = request.get_json()
    token = payload['token']
    handle_str = payload['handle_str']
    return dumps(user.user_profile_sethandle(token, handle_str))
    
@APP.route("/user/profile/uploadphoto", methods=['POST'])
def serv_user_profile_uploadphoto():
    '''show user profile'''
    payload = request.get_json()
    token = payload['token']
    img_url = payload['img_url']
    x_start = payload['x_start']
    x_end = payload['x_end']
    y_start = payload['y_start']
    y_end = payload['y_end']
    return dumps(user.user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end))

@APP.route("/channels/create", methods=['POST'])
def channel_create():
    '''create a new channel'''
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    return dumps(channels.channels_create(token,name,is_public))

@APP.route("/message/send", methods=['POST'])
def message_send():
    '''send message to a channel'''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    msg = payload['message']
    return dumps(message.message_send(token, channel_id, msg))

@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    '''send message to a channel'''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    msg = payload['message']
    time_sent = payload['time_sent']
    return dumps(message.message_sendlater(token, channel_id, msg, time_sent))

@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    '''remove message'''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    return dumps(message.message_remove(token, message_id))

@APP.route("/message/edit", methods=['PUT'])
def message_edit():
    '''edit message'''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    msg = payload['message']
    return dumps(message.message_edit(token, message_id, msg))

@APP.route("/message/pin", methods=['POST'])
def message_pin():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    return dumps(message.message_pin(token, message_id))
    
@APP.route("/message/unpin", methods=['POST'])
def message_unpin():
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    return dumps(message.message_unpin(token, message_id))

# Channel.py flasking
# Channel invite
@APP.route("/channel/invite", methods=['POST'])
def serv_channel_invite():
    ''' invites user to channel'''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    return dumps(channel.channel_invite(token, channel_id, u_id))

@APP.route("/channel/messages", methods=['GET'])
def serv_channel_messages():
    '''return messages'''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    return dumps(channel.channel_messages(token, channel_id, start))

# Channel details
@APP.route("/channel/details", methods=['GET'])
def serv_channel_details():
    ''' returns channel details'''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return dumps(channel.channel_details(token, channel_id))

# Channel join
@APP.route("/channel/join", methods=['POST'])
def serv_channel_join():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    return dumps(channel.channel_join(token, channel_id))

# Channel addowner
@APP.route("/channel/addowner", methods=['POST'])
def serv_channel_addowner():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    return dumps(channel.channel_addowner(token, channel_id, u_id))

# Channel leave
@APP.route("/channel/leave", methods=['POST'])
def serv_channel_leave():
    '''user leaves channel'''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    return dumps(channel.channel_leave(token, channel_id))

# Channel removeowner
@APP.route("/channel/removeowner", methods=['POST'])
def serv_channel_removeowner():
    ''' removes owner'''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    return dumps(channel.channel_removeowner(token, channel_id, u_id))

@APP.route("/message/react", methods=['POST'])
def serv_message_react():
    '''react to a message'''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']
    return dumps(message.message_react(token, message_id, react_id))

@APP.route("/message/unreact", methods=['POST'])
def serv_message_unreact():
    '''cancel react to a message'''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']
    return dumps(message.message_unreact(token, message_id, react_id))

@APP.route("/standup/start",methods=['POST'])
def standup_start():
    ''' standup/start route '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    length = payload['length']
    return dumps(standup.standup_start(token, channel_id, length))

@APP.route("/standup/active",methods=['GET'])
def standup_active():
    ''' standup/active route '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    print(channel_id)
    return dumps(standup.standup_active(token, channel_id))

@APP.route("/standup/send",methods=['POST'])
def standup_send():
    ''' standup/send route '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    return dumps(standup.standup_send(token, channel_id, message))

# auth password reset request
@APP.route("/auth/passwordreset/request", methods=['POST'])
def serv_pswd_request():
    ''' requests code to change password '''
    payload = request.get_json()
    email = payload['email']
    return dumps(auth.pwd_reset_request(email))

# auth password reset
@APP.route("/auth/passwordreset/reset", methods=['POST'])
def serv_pswd_reset():
    ''' requests code to change password '''
    payload = request.get_json()
    reset_code = payload['reset_code']
    new_password = payload['new_password']
    return dumps(auth.pwd_reset_reset(reset_code, new_password))

if __name__ == "__main__":
    APP.run(port=0, debug = True) # Do not edit this 
