from flask import Blueprint, render_template, jsonify, redirect, request, url_for, flash
from application import db
from application.modals import Sponser, Campaign, User, Requests, Posts
from application.form import SponserDetailForm, CampaignDetails, PaymentForm, UpdateCampForm, categories
from application.validation import UserError
from flask_login import login_required, current_user
from sqlalchemy import desc as decend
from application.get_roles import user_roles
from application.hash import checkpw
from werkzeug.utils import secure_filename
from datetime import datetime
from uuid import uuid4
import os


sponser = Blueprint('sponser', __name__)

@sponser.route('/get_sponser_data', methods = ['GET', 'POST'])
@login_required
def get_sponser_data():            
    if 'Sponser' not in user_roles(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    form = SponserDetailForm()
    form.industry.choices = categories
    if form.validate_on_submit():
        try:
            new_sponser = Sponser(sponser_id = current_user.user_id, company_name = form.company_name.data, industry = form.industry.data, budget = int(form.budget.data), about = form.about.data)
            db.session.add(new_sponser)
            db.session.commit()
            flash('New Sponser account has been created :)')
            return redirect(url_for('home.dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(e)

    return render_template('auth/user_details.html', page = 'login', role = 'Sponser',form = form)

@sponser.route('/new/campaign', methods = ['GET', 'POST'])
@login_required
def new_campaign():
    if not Sponser.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    user = User.query.get(current_user.user_id)
    form = CampaignDetails()
    form.category.choices = categories
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
                if form.end_date.data:
                    end_date = str(form.end_date.data).split('-')
                    form.end_date.data = datetime(year = int(end_date[0]), month = int(end_date[1]), day = int(end_date[2]), hour = 23, minute = 59, second = 59)

                new_camp = Campaign(campaign_by = current_user.user_id, campaign_name = form.campaign_name.data, desc = form.desc.data, category = form.category.data, requirements = form.requirements.data, start_date = form.start_date.data, end_date = form.end_date.data, budget = form.budget.data, goals = form.goals.data, image_path = new_image_name, visibility = True if int(form.visibility.data) == 1 else False)
                db.session.add(new_camp)
                db.session.commit()
                if image_file:
                    image_file.save(image_path)
                flash('New Campaign Created')
                return redirect(url_for('home.dashboard'))
            
            except Exception as e:
                db.session.rollback()
                flash(e)
        else:
            flash('Campaign Name must be unique')
    
    return render_template('sponser/new_camp.html',user = user, page = 'Create Campaign', form = form, roles = roles)

@sponser.route('/delete/campaign/<int:campaign_id>', methods = ['GET', 'POST'])
@login_required
def delete_camp(campaign_id):
    if not Sponser.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    camp = Campaign.query.get(campaign_id)
    if camp:
        try:
            db.session.delete(camp)
            db.session.commit()
            return jsonify({'Request' : 'Success'})
        except:
            db.session.rollback()
            return jsonify({'Request' : 'Failed to delete. Try Again'})
    return jsonify({'Request' : 'No such campaign exists'})
    

@sponser.route('/my/campaigns', methods = ['GET', 'POST'])
@login_required
def my_campaigns():
    if not Sponser.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    user = User.query.get(current_user.user_id)
    campaigns = Campaign.query.filter_by(campaign_by = current_user.user_id).order_by(decend(Campaign.start_date)).all()
    return render_template('uni/campaigns.html',user = user, page = 'My Campaigns', roles = 'Sponser', campaigns = campaigns)

@sponser.route('/edit/<int:camp_id>', methods = ['PUT'])
@login_required
def edit_camp(camp_id):
    if not Sponser.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
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
                    db.session.rollback()
                    return jsonify({'Request' : e})
        
            case 'desc':
                try:
                    camp.desc = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Campaign.query.get(camp_id).desc})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
            case 'requirements':
                try:
                    camp.requirements = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Campaign.query.get(camp_id).requirements})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
                
            case 'goals':
                try:
                    camp.goals = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Campaign.query.get(camp_id).goals})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
            
            case 'budget':
                try:
                    camp.budget = int(val)
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Campaign.query.get(camp_id).budget})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})

            case 'visible':
                try:
                    curr_val = Campaign.query.get(camp_id).visibility
                    print(curr_val)
                    camp.visibility = not curr_val
                    db.session.commit()
                    return jsonify({'Request' : 'Success, Reload to see changes', 'new_val' : Campaign.query.get(camp_id).visibility})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
    else:
        return jsonify({'Request' : 'Not Authorised'})
    
@sponser.route('/update_camp/<int:camp_id>', methods = ["GET", "POST"])
@login_required
def update_camp(camp_id):
    if not Sponser.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    form = UpdateCampForm()
    curr_user = User.query.get(current_user.user_id)
    camp = Campaign.query.get(camp_id)
    roles = user_roles(curr_user.user_id)

    if form.validate_on_submit():                       
        if form.start_date.data:
            camp.start_date = form.start_date.data
        
        if form.end_date.data:
            end_date = str(form.end_date.data).split('-')
            form.end_date.data = datetime(year = int(end_date[0]), month = int(end_date[1]), day = int(end_date[2]), hour = 23, minute = 59, second = 59)
            camp.end_date = form.end_date.data

        image_file = request.files['image']
        new_image_name = None
        new_image_path = None

        if image_file:
            unique_name = str(uuid4())
            image_ext = image_file.filename.split('.')[1] #image extension
            new_image_name = unique_name+'.'+image_ext
            image_file.filename = new_image_name
            image_filename = secure_filename(image_file.filename)
            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            upload_folder = os.path.join(base_dir, '..', 'static', 'uploads')
            new_image_path = os.path.join(upload_folder, image_filename)

            #delete old image
            if not camp.image_path == 'user.png':
                old_image_path = os.path.join(upload_folder, camp.image_path)
                os.remove(old_image_path)

            camp.image_path = new_image_name
        
        try:
            db.session.commit()

            if image_file:
                image_file.save(new_image_path) 

            flash('Profile Updated Successfully!')
            return redirect(f'/view/{camp_id}')
        except Exception as e:
            db.session.rollback()
            flash('Something Went Wrong. Try Again\n', e)

    return render_template('sponser/update_camp.html', form = form, user = curr_user, roles = roles, page = 'Update Campaign')
    
@sponser.route('/posts', methods = ['GET', 'POST'])
@login_required
def posts():
    if not Sponser.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    spn = Sponser.query.get(current_user.user_id)
    if not spn:
        raise UserError(401, 'Not Authorised')
    
    roles = user_roles(current_user.user_id)

    rqsts = []
    camps = Campaign.query.filter_by(campaign_by = spn.sponser_id)
    for camp in camps:
        rqsts += [rqst for rqst in Requests.query.filter_by(campaign_id = camp.campaign_id).all()]

    posts = []
    for rqst in rqsts:
        posts += [post for post in Posts.query.filter_by(post_for = rqst.request_id).all()]
    return render_template('uni/posts_dash.html', page = f'Posts for {spn.company_name}', roles = roles, posts = posts)

@sponser.route('/pay/<int:rqst_id>', methods = ['GET', 'POST'])
@login_required
def payment(rqst_id):
    if not Sponser.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    spn = User.query.get(current_user.user_id)
    roles = user_roles(current_user.user_id)
    rqst = Requests.query.get(rqst_id)
    if 'Sponser' in roles or spn.user_id != rqst.campaign.campaign_by:
        pay_to = User.query.get(rqst.influencer_id)
        form = PaymentForm()
        form.amount.label.text = f'Pay ${rqst.n_amount}* for {rqst.campaign.campaign_name}'
        if form.validate_on_submit():
            if form.amount.data == rqst.n_amount:
                if checkpw(form.password.data, spn.password):
                    if spn.wallet_balance >= form.amount.data:
                        try:
                            spn.wallet_balance -= form.amount.data
                            pay_to.wallet_balance += form.amount.data
                            db.session.commit()
                            rqst.status = 'Fullfilled/Paid'
                            db.session.commit()
                            flash('Payment Successful!')
                            return redirect(url_for('home.requests'))
                        except Exception as e:
                            db.session.rollback()
                            flash(e)
                    else:
                        flash('Not Enough Balance')
                else:
                    flash('Wrong Password, Try again.')
            else:
                flash(f'Amount must be equal to negotiated amount: ${rqst.n_amount}')
        return render_template('uni/pay.html', form = form, page = 'Payment', roles = roles)
    else:
        raise UserError(401, 'Unauthorised')