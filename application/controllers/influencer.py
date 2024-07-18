from flask import Blueprint, render_template, jsonify, redirect, request, url_for, flash
from application import db
from application.modals import Sponser, Campaign, User, Influencer, Requests, Posts
from application.form import SponserDetailForm, CampaignDetails, InfluencerDetailForm, PostDetails
from flask_login import login_required, current_user
from sqlalchemy import desc as decend
from application.get_roles import user_roles
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

influencer = Blueprint('influencer', __name__)
                       
@influencer.route('/get_influencer_data', methods = ['GET', 'POST'])
@login_required
def get_influencer_data():
    form = InfluencerDetailForm()

    if form.validate_on_submit():
        try:
            new_inf = Influencer(influencer_id = current_user.user_id, name = form.name.data, category = form.category.data, niche = form.niche.data, about = form.about.data)
            db.session.add(new_inf)
            db.session.commit()
            flash('Influencer account has been created :)')
            return redirect(url_for('home.dashboard'))

        except Exception as e:
            flash(e)

    return render_template('user_details.html', page = 'login', role = 'influencer', form = form)

        
@influencer.route('/new/post', methods = ['GET', 'POST'])
@login_required
def new_post():
    if Influencer.query.get(current_user.user_id):
        form = PostDetails()

        rqsts = Requests.query.filter_by(influencer_id = current_user.user_id).all()
        form.post_for.choices = [None]+[rqst.campaign.campaign_name for rqst in rqsts]
        roles = user_roles(current_user.user_id)

        if form.validate_on_submit():
            post_for = Campaign.query.filter_by(campaign_name = form.post_for.data).first()
            if post_for:
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
                    new_post = Posts(post_by = current_user.user_id, post_for = post_for.campaign_id, post_title = form.post_title.data, desc = form.desc.data, image_path = new_image_name)
                    db.session.add(new_post)
                    db.session.commit()
                    if image_file:
                        image_file.save(image_path)
                    flash('New Campaign Created')
                    return redirect(url_for('home.dashboard'))
                
                except Exception as e:
                    flash(e)       
            else:
                flash('Please Select a Campaign')

        return render_template('new_post.html', user = influencer, page = 'Create Post', form = form, roles = roles)
    else:
        return '<h1>Not Authorised</h1>'

@influencer.route('/my/post', methods = ['GET', 'POST'])
@login_required
def my_post():
    inf = Influencer.query.get(current_user.user_id)
    roles = user_roles(current_user.user_id)
    posts = Posts.query.filter_by(post_by = inf.influencer_id).all()
    return render_template('all_posts.html', user = inf, page = f'{inf.name}\'s Posts', roles = roles, posts = posts)

@influencer.route('/edit/<int:post_id>', methods = ['PUT'])
@login_required
def edit_post(post_id):
    post = Posts.query.get(post_id)
    if post.post_by == current_user.user_id:
        data = request.get_json()
        to_update = data['to_update']
        val = data['value']
        match to_update:
            case 'post_title':
                try:
                    post.post_title = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Posts.query.get(post_id).post_title})
                except Exception as e:
                    return jsonify({'Request' : e})
        
            case 'desc':
                try:
                    post.desc = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Posts.query.get(post_id).desc})
                except Exception as e:
                    return jsonify({'Request' : e})

@influencer.route('/delete/post/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.get(post_id)
    if post:
        try:
            db.session.delete(post)
            db.session.commit()
            return jsonify({'Request' : 'Success'})
        except:
            return jsonify({'Request' : 'Failed to delete. Try Again'})
    return jsonify({'Request' : 'No such post exists'})
    