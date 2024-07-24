from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from application.modals import User, Requests, Influencer, Sponser, Campaign, Posts, Admin, UserRoles
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

@admin.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    roles = user_roles(current_user.user_id)
    camps = Campaign.query.all()
    return render_template('admin/admin_dash.html', page = 'Admin-Dashboard', roles = roles, camps = camps)
    
@admin.route('/users', methods = ["GET","POST"])
@login_required
def users():
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    spn = Sponser.query.all()
    inf = Influencer.query.all()
    roles = user_roles(current_user.user_id)
    return render_template('admin/users.html', sponsers = spn, influencers = inf, page = 'Ongoing Requests', roles = roles)

@admin.route('/requests', methods = ['GET', 'POST'])
@login_required
def requests():
    roles = user_roles(current_user.user_id)
    requests = Requests.query.all()

    return render_template('uni/requests.html', requests = requests, page = 'Requests', roles = roles)

@admin.route('/posts', methods = ["GET","POST"])
@login_required
def posts():
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    roles = user_roles(current_user.user_id)
    posts = Posts.query.all()
    return render_template('uni/posts_dash.html', page = 'Posts', roles = roles, posts = posts)

@admin.route('/approvals', methods = ["GET","POST"])
@login_required
def approvals():
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    
    roles = user_roles(current_user.user_id)
    approval_rqsts = Admin.query.filter_by(approved = False).all()

    users = [User.query.get(user.admin_id) for user in approval_rqsts]
    
    return render_template('admin/approvals.html', page = 'Posts', roles = roles, users = users)

@admin.route('/approvals/<string:action>/<int:admin_id>', methods = ["GET", "POST"])
@login_required
def approval_rqst(action, admin_id):
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    
    user = User.query.get(admin_id)

    if user:
        match action:
            case 'approve':
                admin = Admin.query.get(user.user_id)
                try:
                    if admin:
                        admin.approved = True
                    new_role = UserRoles(user_id = user.user_id, role_id = 1)
                    db.session.add(new_role)
                    db.session.commit()
                    flash('Admin Approved')
                except Exception as e:
                    flash(e)
            
            case 'delete':
                try:
                    db.session.delete(user)
                    db.session.commit()
                    flash('Request deleted')
                except Exception as e:
                    flash(e)

    else:
        flash('No such user')
    return redirect(url_for('admin.approvals'))

    
@admin.route('/activities', methods = ["GET","POST"])
@login_required
def activities():
    if not is_admin(current_user.user_id):
        raise UserError(401, "Not Authorised")
    roles = user_roles(current_user.user_id)
    return render_template('admin/activities.html', page = 'Activities', roles = roles)