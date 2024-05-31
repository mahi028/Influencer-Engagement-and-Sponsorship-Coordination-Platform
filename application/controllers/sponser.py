from flask import Blueprint, render_template, redirect, url_for, flash
from application import db
from application.modals import User, UserRoles, Influencer, Sponser, Campaign
from application.form import SponserDetailForm, CampaignDetails
from application.hash import hashpw, checkpw
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime


sponser = Blueprint('sponser', __name__)

@sponser.route('/get_sponser_data', methods = ['GET', 'POST'])
@login_required
def get_sponser_data():
    if UserRoles.query.get((current_user.user_id, 3)):
        sponser = Sponser.query.get(current_user.user_id)

        if sponser:
            flash(f'Logged in as {sponser.company_name}')
            return redirect(url_for('home.dashboard'))
                
        form = SponserDetailForm()

        if form.validate_on_submit():
            try:
                new_sponser = Sponser(sponser_id = current_user.user_id, company_name = form.company_name.data, industry = form.industry.data, budget = int(form.budget.data))
                db.session.add(new_sponser)
                db.session.commit()
                flash('New Sponser account has been created :)')
                return redirect(url_for('home.dashboard'))

            except Exception as e:
                flash(e)

        return render_template('user_details.html', page = 'login', form = form)
        
    flash('Account with role Sponser does not exists. Try again')
    logout_user()
    return redirect(url_for('user_auth.login'))

@sponser.route('/new/campaign', methods = ['GET', 'POST'])
@login_required
def new_camapign():
    form = CampaignDetails()

    if form.validate_on_submit():
        campaign_name = Campaign.query.filter_by(campaign_name = form.campaign_name.data).first()

        if not campaign_name:
            # try:
                # date = form.end_date.data.strip('-')
                # datetime(year = int(date(0)), month = int(date(1)), day = int(date(2)))

                new_camp = Campaign(campaign_by = current_user.user_id, campaign_name = form.campaign_name.data, desc = form.desc.data, end_date = form.end_date.data, budget = form.budget.data, goals = form.goals.data, visibility = True if int(form.visibility.data) == 1 else False)
                db.session.add(new_camp)
                db.session.commit()
                flash('New Campaign Created')
                return redirect(url_for('home.dashboard'))
            
            # except Exception as e:
            #     flash(e)
        else:
            flash('Campaign Name must be unique')
    
    return render_template('new_camp.html', page = 'Create Campaign', form = form)