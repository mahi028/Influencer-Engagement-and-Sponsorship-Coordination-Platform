from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from application.modals import User, Requests, Influencer, Sponser, Campaign, Posts
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
    return render_template('admin_dash.html', page = 'Admin-Dashboard', roles = roles, camps = camps)

@admin.route('/flag/<string:type>/<int:id>/<string:reason>', methods = ["POST"])
@login_required
def flag(type,id, reason):
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    match type:
        case 'camp':
            post = Campaign.query.get(id)
            post.flag = not post.flag
            db.session.commit()
            post = Campaign.query.get(id)
            if post.flag:
                post.flag_reason = reason
            else:
                post.flag_reason = None
            db.session.commit()
            return jsonify({'Request': 'Success'})
        
        case 'post':
            post = Posts.query.get(id)
            post.flag = not post.flag
            db.session.commit()
            post = Posts.query.get(id)
            if post.flag:
                post.flag_reason = reason
            else:
                post.flag_reason = None
            db.session.commit()
            return jsonify({'Request': 'Success'})
        
        case 'user':
            user = User.query.get(id)
            user.flag = not user.flag
            db.session.commit()
            user = User.query.get(id)
            if user.flag:
                user.flag_reason = reason
            else:
                user.flag_reason = None
            db.session.commit()
            return jsonify({'Request': 'Success'})
    
@admin.route('/users', methods = ["GET","POST"])
@login_required
def users():
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    spn = Sponser.query.all()
    inf = Influencer.query.all()
    roles = user_roles(current_user.user_id)
    return render_template('users.html', sponsers = spn, influencers = inf, page = 'Ongoing Requests', roles = roles)

@admin.route('/posts', methods = ["GET","POST"])
@login_required
def posts():
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    roles = user_roles(current_user.user_id)
    posts = Posts.query.all()
    return render_template('admin_dash_posts.html', page = 'Posts', roles = roles, posts = posts)
    
@admin.route('/activities', methods = ["GET","POST"])
@login_required
def activities():
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    roles = user_roles(current_user.user_id)
    return render_template('activities.html', page = 'Activities', roles = roles)