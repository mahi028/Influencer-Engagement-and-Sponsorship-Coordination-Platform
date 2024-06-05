from flask import Blueprint, render_template, redirect, url_for, flash
from application.modals import User, UserRoles, Requests, Influencer, Sponser, Campaign
from flask_login import login_required, current_user
from sqlalchemy import desc

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
    
    return render_template('dashboard.html', page = 'Dashboard', roles = roles, campaigns = campaigns)

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
    
    return render_template('dashboard.html', page = 'Requests', roles = roles, rqst = rqst, my_rqst = my_rqst)