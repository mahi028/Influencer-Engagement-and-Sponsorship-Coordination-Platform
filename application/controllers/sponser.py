from flask import Blueprint, render_template, jsonify, redirect, request, url_for, flash
from application import db
from application.modals import Sponser, Campaign, Requests, User
from application.form import SponserDetailForm, CampaignDetails
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from uuid import uuid4
import os


sponser = Blueprint('sponser', __name__)

@sponser.route('/get_sponser_data', methods = ['GET', 'POST'])
@login_required
def get_sponser_data():            
    form = SponserDetailForm()

    if form.validate_on_submit():
        try:
            new_sponser = Sponser(sponser_id = current_user.user_id, company_name = form.company_name.data, industry = form.industry.data, budget = int(form.budget.data), about = form.about.data)
            db.session.add(new_sponser)
            db.session.commit()
            flash('New Sponser account has been created :)')
            return redirect(url_for('home.dashboard'))

        except Exception as e:
            flash(e)

    return render_template('user_details.html', page = 'login', role = 'sponser',form = form)

@sponser.route('/new/campaign', methods = ['GET', 'POST'])
@login_required
def new_campaign():
    user = User.query.get(current_user.user_id)
    form = CampaignDetails()

    if form.validate_on_submit():
        campaign_name = Campaign.query.filter_by(campaign_name = form.campaign_name.data).first()

        if not campaign_name:
            image_file = request.files['image']
            new_image_name = None
            image_path = None
            if image_file:
            # Create unique name for image
                unique_name = str(uuid4())
                image_ext = image_file.filename.split('.')[1] #image extension
                new_image_name = unique_name+'.'+image_ext
                image_file.filename = new_image_name
                image_filename = secure_filename(image_file.filename)
                
                base_dir = os.path.dirname(os.path.abspath(__file__))
                upload_folder = os.path.join(base_dir, '..', 'static', 'uploads')
                image_path = os.path.join(upload_folder, image_filename)
            try:
                new_camp = Campaign(campaign_by = current_user.user_id, campaign_name = form.campaign_name.data, desc = form.desc.data, end_date = form.end_date.data, budget = form.budget.data, goals = form.goals.data, image_path = new_image_name, visibility = True if int(form.visibility.data) == 1 else False)
                db.session.add(new_camp)
                db.session.commit()
                if image_file:
                    image_file.save(image_path)
                flash('New Campaign Created')
                return redirect(url_for('home.dashboard'))
            
            except Exception as e:
                flash(e)
        else:
            flash('Campaign Name must be unique')
    
    return render_template('new_camp.html',user = user, page = 'Create Campaign', form = form)

@sponser.route('/delete/campaign/<int:campaign_id>', methods = ['GET', 'POST'])
@login_required
def delete_camp(campaign_id):
    camp = Campaign.query.get(campaign_id)
    if camp:
        try:
            db.session.delete(camp)
            db.session.commit()
            return jsonify({'Request' : 'Success'})
        except:
            return jsonify({'Request' : 'Failed to delete. Try Again'})
    return jsonify({'Request' : 'No such campaign exists'})
    

@sponser.route('/my/campaigns', methods = ['GET', 'POST'])
@login_required
def my_campaigns():
    user = User.query.get(current_user.user_id)
    campaigns = Campaign.query.filter_by(campaign_by = current_user.user_id).all()
    return render_template('dashboard.html',user = user, page = 'My Campaigns', roles = 'Sponser', campaigns = campaigns)