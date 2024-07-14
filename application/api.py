from flask_restful import Resource, reqparse, marshal_with, fields
from flask import jsonify
from application.modals import *
from application.validation import UserError
from application.modals import User
from datetime import datetime

user_parser = reqparse.RequestParser()
user_parser.add_argument('email')

activity_fields = {
    "status" : fields.String,
}

class Activities(Resource):
    def get(self, type_of_data):

        match type_of_data:
            case 'request_stats':
                requests = Requests.query.all()
                data = {}
                for rqst in requests:
                    if rqst.status not in data:
                        data[rqst.status] = 0
                    data[rqst.status] += 1

                return jsonify(data)
            
            case 'active_camps':
                data = {}
                data['flag'] = Campaign.query.filter_by(flag = True).count()
                data['active'] = Campaign.query.filter(Campaign.start_date <= datetime.utcnow(), Campaign.end_date >= datetime.utcnow(), Campaign.flag == False).count()
                data['unactive'] = len(Campaign.query.all()) - data['flag'] - data['active']

                return jsonify(data)
            
            case 'active_users':
                data = {}
                data['flag'] = User.query.filter_by(flag = True).count()
                data['un-flag'] = len(User.query.all()) - data['flag']

                return jsonify(data)            