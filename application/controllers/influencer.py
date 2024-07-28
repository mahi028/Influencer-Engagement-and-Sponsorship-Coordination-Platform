from flask import Blueprint, render_template, jsonify, redirect, request, url_for, flash
from application import db
from application.modals import Campaign, User, Influencer, Requests, Posts
from application.form import InfluencerDetailForm, PostDetails, UpdatePostForm, categories
from application.validation import UserError
from flask_login import login_required, current_user
from sqlalchemy import desc as decend
from application.get_roles import user_roles
from werkzeug.utils import secure_filename
from datetime import datetime
from uuid import uuid4
import os

influencer = Blueprint('influencer', __name__)
                       
@influencer.route('/get_influencer_data', methods = ['GET', 'POST'])
@login_required
def get_influencer_data():
    if 'Influencer' not in user_roles(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    form = InfluencerDetailForm()
    form.category.choices = categories
    
    if form.validate_on_submit():
        try:
            new_inf = Influencer(influencer_id = current_user.user_id, name = form.name.data, category = form.category.data, about = form.about.data)
            db.session.add(new_inf)
            db.session.commit()
            flash('Influencer account has been created :)')
            return redirect(url_for('home.dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(e)

    return render_template('auth/user_details.html', page = 'login', role = 'Influencer', form = form)

        
@influencer.route('/new/post', methods = ['GET', 'POST'])
@login_required
def new_post():
    if not Influencer.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    form = PostDetails()

    rqsts = Requests.query.filter_by(influencer_id = current_user.user_id, status = 'Accepted/Ongoing').all()
    if rqsts:
        form.post_for.choices = [None]+[rqst.campaign.campaign_name for rqst in rqsts if rqst.campaign.start_date < datetime.utcnow() and rqst.campaign.end_date > datetime.utcnow()]
    else:
        form.post_for.choices = [None]

    roles = user_roles(current_user.user_id)

    if form.validate_on_submit():
        post_camp = Campaign.query.filter_by(campaign_name = form.post_for.data).first()
        post_for = None

        if post_camp:
            post_for = Requests.query.filter_by(campaign_id = post_camp.campaign_id, influencer_id = current_user.user_id).first().request_id

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
            new_post = Posts(post_by = current_user.user_id, post_for = post_for, post_title = form.post_title.data, desc = form.desc.data, image_path = new_image_name, approved = True if not post_for else False, visibility = False if post_for else True)
            db.session.add(new_post)
            db.session.commit()
            if image_file:
                image_file.save(image_path)
            flash('New Post Created')
            return redirect(url_for('home.dashboard'))
        
        except Exception as e:
            db.session.rollback()
            flash(e)

    return render_template('influencer/new_post.html', user = influencer, page = 'Create Post', form = form, roles = roles)

@influencer.route('/my/post', methods = ['GET', 'POST'])
@login_required
def my_post():
    if not Influencer.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    inf = Influencer.query.get(current_user.user_id)
    roles = user_roles(current_user.user_id)
    posts = Posts.query.filter_by(post_by = inf.influencer_id).order_by(decend(Posts.post_id)).all()
    return render_template('uni/all_posts.html', user = inf, page = f'{inf.name}\'s Posts', roles = roles, posts = posts)

@influencer.route('/edit/<int:post_id>', methods = ['PUT'])
@login_required
def edit_post(post_id):
    if not Influencer.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
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
                    db.session.rollback()
                    return jsonify({'Request' : e})

            case 'desc':
                try:
                    post.desc = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Posts.query.get(post_id).desc})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
                
            case 'visible':
                try:
                    curr_val = Posts.query.get(post_id).visibility
                    if post.approved:
                        post.visibility = not curr_val
                        db.session.commit()
                        return jsonify({'Request' : 'Success, Reload to see changes'})
                    else:
                        return jsonify({'Request' : 'Post has not been approved by the Sponser yet.'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
                
    elif post.request.campaign.campaign_by == current_user.user_id:
        data = request.get_json()
        to_update = data['to_update']
        val = data['value']
        match to_update:
            case 'approved':
                try:
                    post.approved = True
                    db.session.commit()
                    return jsonify({'Request' : 'Success, Reload to see Changes'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})

@influencer.route('/update_post/<int:post_id>', methods = ["GET", "POST"])            
@login_required
def update_post(post_id):
    if not Influencer.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    form = UpdatePostForm()
    curr_user = User.query.get(current_user.user_id)
    post = Posts.query.get(post_id)
    roles = user_roles(curr_user.user_id)

    if form.validate_on_submit():
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
            if not post.image_path == 'user.png':
                old_image_path = os.path.join(upload_folder, post.image_path)
                os.remove(old_image_path)

            post.image_path = new_image_name
        
        try:
            db.session.commit()

            if image_file:
                image_file.save(new_image_path) 

            flash('Profile Updated Successfully!')
            return redirect(f'/view/post/{post_id}')
        except Exception as e:
            db.session.rollback()
            flash('Something Went Wrong. Try Again\n', e)

    return render_template('influencer/update_post.html', form = form, user = curr_user, roles = roles, page = 'Update Post')

@influencer.route('/delete/post/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def delete_post(post_id):
    if not Influencer.query.get(current_user.user_id):
        raise UserError(401, 'Not Authorised')
    
    post = Posts.query.get(post_id)
    if post:
        try:
            db.session.delete(post)
            db.session.commit()
            return jsonify({'Request' : 'Success'})
        except:
            db.session.rollback()
            return jsonify({'Request' : 'Failed to delete. Try Again'})
    return jsonify({'Request' : 'No such post exists'})