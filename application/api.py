from flask_restful import Resource, reqparse, marshal_with, fields
from flask import jsonify
from application.modals import *
from application.validation import UserError
from application.hash import hashpw, checkpw
from application.modals import User

user_parser = reqparse.RequestParser()
user_parser.add_argument('email')
user_parser.add_argument('password')
user_parser.add_argument('confirm_password')

class CampRequests(Resource):
    def post(self, campaign_by):
        # if campaign_by == user_id:
        #     return UserError(status_code=401, error_msg="")
        # pass
        pass
            