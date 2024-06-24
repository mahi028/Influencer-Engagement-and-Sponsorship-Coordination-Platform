from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from application.modals import User, Requests, Influencer, Sponser, Campaign
from application.form import UpdateProfileForm, SeachForm
from flask_login import login_required, current_user
from sqlalchemy import desc as decend
from application import db
from application.hash import hashpw
from application.get_roles import user_roles
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

home = Blueprint('home',__name__)

@home.route('/')
def landing_page():
    return render_template('landing.html', page = 'Welcome')

@home.route('/dashboard')
@login_required
def dashboard():
    roles = user_roles(current_user.user_id)

    if 'Sponser' in roles:
        sponser_details = Sponser.query.get(current_user.user_id)
        if not sponser_details:
            return redirect(url_for('sponser.get_sponser_data'))
    
    if 'Influencer' in roles:
        inf_details = Influencer.query.get(current_user.user_id)
        if not inf_details:
            return redirect(url_for('influencer.get_influencer_data'))
        
    campaigns = Campaign.query.filter_by(visibility = True).order_by(decend(Campaign.start_date)).all()
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
    roles = user_roles(current_user.user_id)

    campaigns = Campaign.query.filter_by(campaign_by = current_user.user_id).all()
    rqst = []
    if campaigns:
        for campaign in campaigns:
            rq = Requests.query.filter_by(campaign_id = campaign.campaign_id).all()
            for r in rq:
                rqst.append(r)
    my_rqst = Requests.query.filter_by(influencer_id = current_user.user_id).all()
    user = User.query.get(current_user.user_id)    
    return render_template('dashboard.html', page = 'Requests', roles = roles, rqst = rqst, my_rqst = my_rqst, user = user)

@home.route('/edit/<string:user>', methods = ['PUT'])
@login_required
def profile_edit(user):
    data = request.get_json()
    to_update = data['to_update']
    val = data['value']

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
                    return jsonify({'Request' : 'Success', 'new_val' : Sponser.query.get(current_user.user_id).industry})
                except Exception as e:
                    return jsonify({'Request' : e})
            case 'about':
                try:
                    curr_user.about = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Sponser.query.get(current_user.user_id).about})
                except Exception as e:
                    return jsonify({'Request' : e})
                
@home.route('/update_imp', methods = ["GET", "POST"])
@login_required
def update_imp():
    form = UpdateProfileForm()
    curr_user = User.query.get(current_user.user_id)
    if form.validate_on_submit():

        if form.email.data:
            if not User.query.filter_by(email = form.email.data).first():
                curr_user.email = form.email.data
            else:
                flash('Email Already Exists.')
        
        if form.password.data:
            if form.conf_password.data:
                if form.password.data == form.conf_password.data:
                    curr_user.password = hashpw(form.password.data)
                else:
                    flash('Password did not match')
                    return redirect(url_for('home.update_imp'))                    
            else:
                flash('Plese fill conf_password feild')
                return redirect(url_for('home.update_imp'))                    
        
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
            old_image_path = os.path.join(upload_folder, curr_user.profile)
            os.remove(old_image_path)

            curr_user.profile = new_image_name
        
        try:
            db.session.commit()

            if image_file:
                image_file.save(new_image_path) 

            flash('Profile Updated Successfully!')
            return redirect(url_for('home.profile'))
        except Exception as e:
            flash('Something Went Wrong. Try Again\n', e)

    return render_template('update_user.html', user = curr_user, form = form)

@home.route('/search', methods = ["GET", "POST"])
def search():
    form = SeachForm()
    if form.validate_on_submit():
        searched = form.search.data 

        user = User.query.filter_by(email = searched).first()
        if user:
            return redirect(f'/get/{user.user_id}') 
        sponser = Sponser.query.filter(Sponser.company_name.like('%'+searched+'%')).all()
        influencer = Influencer.query.filter(Influencer.name.like('%'+searched+'%')).all()
        camps_by_name = Campaign.query.filter(Campaign.campaign_name.like('%'+searched+'%')).all()
        camps_by_desc = Campaign.query.filter(Campaign.desc.like('%'+searched+'%')).all()

        return render_template('searched.html', camps_by_name = camps_by_name, camps_by_desc = camps_by_desc, sponser = sponser, influencer = influencer)
 

@home.route('/view/<int:camp_id>', methods = ["GET", "POST"])
@login_required
def view_camp(camp_id):
    user = User.query.get(current_user.user_id)
    camp = Campaign.query.get(camp_id)
    roles = user_roles(current_user.user_id)

    return render_template('campaign.html', camp = camp, user = user, roles = roles)

@home.route('/get/<int:user_id>', methods = ["GET", "POST"])
@login_required
def get_user(user_id):
    inf = spn = None
    roles = user_roles(user_id)
    if 'Sponser' in roles:
        roles = 'Sponser'
        spn = Sponser.query.get(user_id)

    elif 'Influencer' in roles:
        roles = 'Influencer'
        inf = Influencer.query.get(user_id)

    return render_template('profile.html', role = [roles], inf = inf, spn = spn, page = 'Profile')