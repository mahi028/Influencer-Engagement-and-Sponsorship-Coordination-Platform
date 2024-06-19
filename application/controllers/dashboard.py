from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from application.modals import User, UserRoles, Requests, Influencer, Sponser, Campaign
from flask_login import login_required, current_user
from sqlalchemy import desc
from application import db

home = Blueprint('home',__name__)

@home.route('/')
def landing_page():
    return render_template('landing.html', page = 'Welcome')

@home.route('/dashboard')
@login_required
def dashboard():
    user_roles = UserRoles.query.filter_by(user_id = current_user.user_id).all()
    available_roles = {1: 'Admin', 2: 'Influencer', 3: 'Sponser'}
    roles = [available_roles[role.role_id] for role in user_roles]

    if 'Sponser' in roles:
        sponser_details = Sponser.query.get(current_user.user_id)
        if not sponser_details:
            return redirect(url_for('sponser.get_sponser_data'))
    
    if 'Influencer' in roles:
        inf_details = Influencer.query.get(current_user.user_id)
        if not inf_details:
            return redirect(url_for('influencer.get_influencer_data'))
        
    campaigns = Campaign.query.filter_by(visibility = True).order_by(desc(Campaign.start_date)).all()
    user = User.query.get(current_user.user_id)
    
    return render_template('dashboard.html', page = 'Dashboard', roles = roles, campaigns = campaigns, user = user)

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    user = User.query.get(current_user.user_id)
    camps = Campaign.query.all()
    active_users = User.query.filter_by(is_active = True)
    return render_template('admin_dash.html', page = 'Admin-Dashboard', active_users = active_users, user = user, camps = camps)

@home.route('/requests', methods = ['GET', 'POST'])
@login_required
def requests():
    user_roles = UserRoles.query.filter_by(user_id = current_user.user_id).all()
    available_roles = {1: 'Admin', 2: 'Influencer', 3: 'Sponser'}
    roles = [available_roles[role.role_id] for role in user_roles]

    campaigns = Campaign.query.filter_by(campaign_by = current_user.user_id).all()
    rqst = []
    if campaigns:
        for campaign in campaigns:
            rq = Requests.query.filter_by(campaign_id = campaign.campaign_id).all()
            for r in rq:
                rqst.append(r)
    my_rqst = Requests.query.filter_by(influencer_id = current_user.user_id)
    user = User.query.get(current_user.user_id)    
    return render_template('dashboard.html', page = 'Requests', roles = roles, rqst = rqst, my_rqst = my_rqst, user = user)

@home.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.user_id)
    user_roles = UserRoles.query.filter_by(user_id = current_user.user_id).all()
    available_roles = {1: 'Admin', 2: 'Influencer', 3: 'Sponser'}
    roles = [available_roles[role.role_id] for role in user_roles]
    inf = None
    spn = None

    if 'Influencer' in roles:
        inf = Influencer.query.get(current_user.user_id)
    
    if 'Sponser' in roles:
        spn = Sponser.query.get(current_user.user_id)

    return render_template('profile.html', roles = roles, user = user, inf = inf, spn = spn, page = 'Profile')

@home.route('/edit/<string:user>', methods = ['POST'])
@login_required
def profile_edit(user):
    data = request.get_json()
    to_update = data['to_update']
    val = data['value']
    if user == user:
        curr_user = User.query.get(current_user.user_id)
        match to_update:
            case 'email':
                try:
                    curr_user.email = val 
                    db.session.commit() 
                    return jsonify({'Request' : 'Success', 'new_val' : User.query.get(current_user.user_id).email})
                except Exception as e:
                    return jsonify({'Request' : e})

    if user == 'inf':
        curr_user = Influencer.query.get(current_user.user_id)
        match to_update:
            case 'name':
                try:
                    curr_user.name = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Influencer.query.get(current_user.user_id).name})
                except Exception as e:
                    return jsonify({'Request' : e})
            case 'category':
                try:
                    curr_user.category = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Influencer.query.get(current_user.user_id).category})
                except Exception as e:
                    return jsonify({'Request' : e})
            case 'about':
                try:
                    curr_user.about = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Influencer.query.get(current_user.user_id).about})
                except Exception as e:
                    return jsonify({'Request' : e})

    elif user == 'spn':
        curr_user = Sponser.query.get(current_user.user_id)
        match to_update:
            case 'name':
                try:
                    curr_user.company_name = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Sponser.query.get(current_user.user_id).company_name})
                except Exception as e:
                    return jsonify({'Request' : e})
            case 'category':
                try:
                    curr_user.industry = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Influencer.query.get(current_user.user_id).industry})
                except Exception as e:
                    return jsonify({'Request' : e})
            case 'about':
                try:
                    curr_user.about = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Sponser.query.get(current_user.user_id).about})
                except Exception as e:
                    return jsonify({'Request' : e})