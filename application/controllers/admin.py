from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from application.modals import User, Requests, Influencer, Sponser, Campaign
from application.form import UpdateProfileForm, SeachForm
from flask_login import login_required, current_user
from sqlalchemy import desc as decend
from application import db
from application.hash import hashpw
from application.validation import UserError
from application.get_roles import user_roles, is_admin
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

admin = Blueprint('admin',__name__)


@admin.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    roles = user_roles(current_user.user_id)
    camps = Campaign.query.all()
    active_users = User.query.filter_by(is_active = True)
    return render_template('admin_dash.html', page = 'Admin-Dashboard', active_users = active_users, roles = roles, camps = camps)

@admin.route('/flag/<string:type>/<int:id>', methods = ["POST"])
@login_required
def flag(type,id):
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    match type:
        case 'camp':
            camp = Campaign.query.get(id)
            camp.flag = not camp.flag
            db.session.commit()
            return jsonify({'Request': 'Success'})
        
        case 'user':
            user = User.query.get(id)
            user.flag = not user.flag
            db.session.commit()
            return jsonify({'Request': 'Success'})
    
@admin.route('/requests', methods = ["GET","POST"])
@login_required
def requests():
    rqst = Requests.query.all()
    roles = user_roles(current_user.user_id)
    return render_template('requests.html', requests = rqst, page = 'Ongoing Requests', roles = roles)
    
@admin.route('/activities', methods = ["GET","POST"])
@login_required
def activities():
    roles = user_roles(current_user.user_id)
    return render_template('activities.html', page = 'Activities', roles = roles)