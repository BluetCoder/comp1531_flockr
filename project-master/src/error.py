''' access and input errors '''
from werkzeug.exceptions import HTTPException
class AccessError(HTTPException):
    ''' access error '''
    code = 400
    message = 'No message specified'

class InputError(HTTPException):
    ''' input error'''
    code = 400
    message = 'No message specified'
