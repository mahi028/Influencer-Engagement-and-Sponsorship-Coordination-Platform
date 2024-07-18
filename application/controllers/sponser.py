from flask import Blueprint, render_template, jsonify, redirect, request, url_for, flash
from application import db
from application.modals import Sponser, Campaign, User, Influencer, Requests
from application.form import SponserDetailForm, CampaignDetails
from flask_login import login_required, current_user
from sqlalchemy import desc as decend
from application.get_roles import user_roles
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
    roles = user_roles(current_user.user_id)

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
                new_camp = Campaign(campaign_by = current_user.user_id, campaign_name = form.campaign_name.data, desc = form.desc.data, requirements = form.requirements.data, start_date = form.start_date.data, end_date = form.end_date.data, budget = form.budget.data, goals = form.goals.data, image_path = new_image_name, visibility = True if int(form.visibility.data) == 1 else False)
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
    
    return render_template('new_camp.html',user = user, page = 'Create Campaign', form = form, roles = roles)

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
    campaigns = Campaign.query.filter_by(campaign_by = current_user.user_id).order_by(decend(Campaign.start_date)).all()
    return render_template('dashboard.html',user = user, page = 'My Campaigns', roles = 'Sponser', campaigns = campaigns)

@sponser.route('/edit/<int:camp_id>', methods = ['PUT'])
@login_required
def edit_camp(camp_id):
    camp = Campaign.query.get(camp_id)
    if camp.campaign_by == current_user.user_id:
        data = request.get_json()
        to_update = data['to_update']
        val = data['value']
        match to_update:
            case 'name':
                try:
                    if Campaign.query.filter_by(campaign_name = val).first():
                        return jsonify({'Request' : "Campaign Already Exist"})
                    camp.campaign_name = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Campaign.query.get(camp_id).campaign_name})
                except Exception as e:
                    return jsonify({'Request' : e})
        
            case 'desc':
                try:
                    camp.desc = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Campaign.query.get(camp_id).desc})
                except Exception as e:
                    return jsonify({'Request' : e})
            case 'requirements':
                try:
                    camp.requirements = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Campaign.query.get(camp_id).requirements})
                except Exception as e:
                    return jsonify({'Request' : e})
                
            case 'goals':
                try:
                    camp.goals = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Campaign.query.get(camp_id).goals})
                except Exception as e:
                    return jsonify({'Request' : e})
            
            case 'budget':
                try:
                    camp.budget = int(val)
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Campaign.query.get(camp_id).budget})
                except Exception as e:
                    return jsonify({'Request' : e})

            case 'visible':
                try:
                    curr_val = Campaign.query.get(camp_id).visibility
                    print(curr_val)
                    camp.visibility = not curr_val
                    db.session.commit()
                    return jsonify({'Request' : 'Success, Reload to see changes', 'new_val' : Campaign.query.get(camp_id).visibility})
                except Exception as e:
                    return jsonify({'Request' : e})
    else:
        return jsonify({'Request' : 'Not Authorised'})