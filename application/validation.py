from werkzeug.exceptions import HTTPException
from flask import make_response

class UserError(HTTPException):
    def __init__(self, status_code : int, error_msg : str) -> HTTPException:
        response = {'error_msg' : error_msg}
        self.response = make_response(response, status_code)