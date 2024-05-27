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

class User(Resource):
    def post(self):
        email = user_parser.parse_args().get('email')
        password = user_parser.parse_args().get('password')
        confirm_password = user_parser.parse_args().get('confirm_password')

        user = User.query.filter_by(email = email)

        # if user:
            