from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from application.modals import User, Requests, Influencer, Sponser, Campaign, Admin, Posts, LikedPost
from application.form import UpdateProfileForm, SeachForm, NegotiateForm, PaymentForm, SuggestionForm
from flask_login import login_required, current_user
from sqlalchemy import desc as decend
from application import db
from application.hash import hashpw, checkpw
from application.validation import UserError
from application.get_roles import user_roles
from werkzeug.utils import secure_filename
from uuid import uuid4
from datetime import datetime
import os

home = Blueprint('home',__name__)

@home.route('/')
def landing_page():
    return render_template('landing.html', page = 'Welcome')

@home.route('/all/camps', methods = ['GET', 'POST'])
@login_required
def all_camps():
    roles = user_roles(current_user.user_id)

    if 'Sponser' in roles:
        sponser_details = Sponser.query.get(current_user.user_id)
        if not sponser_details:
            return redirect(url_for('sponser.get_sponser_data'))
    
    if 'Influencer' in roles:
        inf_details = Influencer.query.get(current_user.user_id)
        if not inf_details:
            return redirect(url_for('influencer.get_influencer_data'))
        
    campaigns = Campaign.query.filter(Campaign.start_date <= datetime.utcnow(), Campaign.end_date >= datetime.utcnow(), Campaign.flag == False, Campaign.visibility == True).order_by(decend(Campaign.campaign_id)).all()
    user = User.query.get(current_user.user_id)
    
    return render_template('uni/campaigns.html', page = 'Campaigns', roles = roles, campaigns = campaigns, user = user)

@home.route('/dashboard')
@login_required
def dashboard():
    posts = Posts.query.filter(Posts.visibility == True).order_by(decend(Posts.post_id)).all()
    roles = user_roles(current_user.user_id)
    return render_template('uni/all_posts.html', page = 'Posts', roles = roles, posts = posts)

@home.route('/requests', methods = ['GET', 'POST'])
@login_required
def requests():
    roles = user_roles(current_user.user_id)
    requests = []

    if 'Sponser' in roles:
        all_camps = Campaign.query.filter_by(campaign_by = current_user.user_id).all()
        for camp in all_camps:
            requests += [rqst for rqst in Requests.query.filter_by(campaign_id = camp.campaign_id).all()]
    else:
        requests = Requests.query.filter_by(influencer_id = current_user.user_id).all()

    return render_template('uni/requests.html', requests = requests, page = 'Requests', roles = roles)

@home.route('/edit/<string:user>', methods = ['PUT'])
@login_required
def profile_edit(user):
    data = request.get_json()
    to_update = data['to_update']
    val = data['value']

    if user == 'inf':
        if not Influencer.query.get(current_user.user_id):
            raise UserError(401, 'Not Authorised')
    
        curr_user = Influencer.query.get(current_user.user_id)
        match to_update:
            case 'name':
                try:
                    curr_user.name = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Influencer.query.get(current_user.user_id).name})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
            case 'category':
                try:
                    curr_user.category = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Influencer.query.get(current_user.user_id).category})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
            case 'about':
                try:
                    curr_user.about = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Influencer.query.get(current_user.user_id).about})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})

    elif user == 'spn':
        if not Sponser.query.get(current_user.user_id):
            raise UserError(401, 'Not Authorised')
    
        curr_user = Sponser.query.get(current_user.user_id)
        match to_update:
            case 'name':
                try:
                    curr_user.company_name = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Sponser.query.get(current_user.user_id).company_name})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
            case 'category':
                try:
                    curr_user.industry = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Sponser.query.get(current_user.user_id).industry})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
            case 'about':
                try:
                    curr_user.about = val
                    db.session.commit()
                    return jsonify({'Request' : 'Success', 'new_val' : Sponser.query.get(current_user.user_id).about})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
                
@home.route('/update_imp', methods = ["GET", "POST"])
@login_required
def update_imp():
    form = UpdateProfileForm()
    roles = user_roles(current_user.user_id)
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
                flash('Please fill conf_password feild')
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
            if not curr_user.profile == 'user.png':
                old_image_path = os.path.join(upload_folder, curr_user.profile)
                os.remove(old_image_path)

            curr_user.profile = new_image_name
        
        try:
            db.session.commit()

            if image_file:
                image_file.save(new_image_path) 

            flash('Profile Updated Successfully!')
            return redirect(f'/get/{current_user.user_id}')
        except Exception as e:
            db.session.rollback()
            flash('Something Went Wrong. Try Again\n', e)

    return render_template('auth/update_user.html', user = curr_user, roles = roles, form = form)

@home.route('/search', methods = ["GET", "POST"])
@login_required
def search():
    roles = user_roles(current_user.user_id)
    form = SeachForm()
    if form.validate_on_submit():
        searched = form.search.data 
        if len(searched) < 3:
            return render_template('uni/searched.html')

        user = User.query.filter_by(email = searched).first()
        if user:
            return redirect(f'/get/{user.user_id}') 
        
        sponser = Sponser.query.filter(Sponser.company_name.like('%'+searched+'%')).all()
        influencer = Influencer.query.filter(Influencer.name.like('%'+searched+'%')).all()
        camps_by_category = Campaign.query.filter(Campaign.category.like('%'+searched+'%')).all()
        camps_by_name = Campaign.query.filter(Campaign.campaign_name.like('%'+searched+'%')).all()
        camps_by_desc = Campaign.query.filter(Campaign.desc.like('%'+searched+'%')).all()

        return render_template('uni/searched.html', roles = roles, searched = searched, camps_by_category = camps_by_category, camps_by_name = camps_by_name, camps_by_desc = camps_by_desc, sponser = sponser, influencer = influencer)
 

@home.route('/view/<int:camp_id>', methods = ["GET", "POST"])
@login_required
def view_camp(camp_id):
    user = User.query.get(current_user.user_id)
    camp = Campaign.query.get(camp_id)
    roles = user_roles(current_user.user_id)

    if camp.flag and camp.sponser.user.flag and not (camp.campaign_by == current_user.user_id or 'Admin' in roles):
        flash('No Such Campign')
        return redirect(url_for('home.all_camps'))

    if camp.end_date < datetime.utcnow() and not (camp.campaign_by == current_user.user_id or 'Admin' in roles):
        flash('Campaign is either expired or has not started yet.')
        return redirect(url_for('home.all_camps'))

    return render_template('sponser/campaign.html', camp = camp, user = user, roles = roles)

@home.route('/view/post/<int:post_id>', methods = ["GET", "POST"])
@login_required
def view_post(post_id):
    user = User.query.get(current_user.user_id)
    post = Posts.query.get(post_id)
    liked_by = LikedPost.query.filter_by(post_id = post.post_id).all()
    liked = True if LikedPost.query.get((current_user.user_id, post.post_id)) else False
    roles = user_roles(current_user.user_id)
    if post.flag and post.influencer.user.flag and not (post.post_by == current_user.user_id or 'Admin' in roles):
        return 'Post Not Found'
    
    suggest_form = SuggestionForm()
    if suggest_form.validate_on_submit():
        try:
            if not post.suggestion:
                post.suggestion = ' '
                db.session.commit()
            post.suggestion += " | "+suggest_form.suggest.data
            db.session.commit()
            flash('Suggestion Made')
            post = Posts.query.get(post_id)
        except Exception as e:
            db.session.rollback()
            flash(e)

    return render_template('influencer/post.html', post = post, liked_by = liked_by, likes = len(liked_by), liked = liked, user = user, roles = roles, suggest_form = suggest_form)

@home.route('/get/<int:user_id>', methods = ["GET", "POST"])
@login_required
def get_user(user_id):
    inf = spn = adm = None
    roles = user_roles(user_id)
    curr_user_roles = user_roles(current_user.user_id)
    camps = None
    user_profile = User.query.get(user_id)

    if user_profile.flag and not (user_profile.user_id == current_user.user_id or 'Admin' in curr_user_roles):
        return "No user exist"

    if 'Sponser' in roles:
        roles = 'Sponser'
        spn = Sponser.query.get(user_id)

    elif 'Influencer' in roles:
        roles = 'Influencer'
        inf = Influencer.query.get(user_id)

        if 'Sponser' in curr_user_roles:
            camps = Campaign.query.filter_by(campaign_by = current_user.user_id).all()

    elif 'Admin' in roles:
        roles = 'Admin'
        adm = Admin.query.get(user_id)

    return render_template('uni/profile.html', profile = user_profile, roles = curr_user_roles, role = [roles], inf = inf, spn = spn, adm = adm, camps = camps, page = 'Profile')

@home.route('/send/rqst/<int:inf_id>/<int:camp_id>')
@login_required
def send_rqst(inf_id, camp_id):
    inf = Influencer.query.get(inf_id)
    camp = Campaign.query.get(camp_id)
    roles = user_roles(current_user.user_id)
    if 'Admin' not in roles: 
        if inf and camp:
            if Requests.query.filter_by(campaign_id = camp.campaign_id, influencer_id = inf.influencer_id).first():
                flash('Request already exists.')
            else:
                try:
                    new_rqst = Requests(campaign_id = camp.campaign_id, influencer_id = inf.influencer_id, n_amount = camp.budget, requested_by = roles[0])
                    db.session.add(new_rqst)
                    db.session.commit()
                    flash('Request Made')
                    return redirect(url_for('home.requests'))
                except Exception as e:
                    db.session.rollback()
                    flash(e)
        else:
            flash('No such Influencer or Campaign')
        if 'Influencer' in roles:
            return redirect(f'/view/{camp.campaign_id}')
        else:
            return redirect(f'/get/{inf.influencer_id}')

    flash('Admin Can\'t Colab')
    return redirect(url_for('admin.admin_dashboard'))

@home.route('/negotiate/<int:rqst_id>', methods = ['GET', 'POST'])
@login_required
def negotiate(rqst_id):
    rqst = Requests.query.get(rqst_id)
    if rqst.status == 'Pending':
        roles = user_roles(current_user.user_id)
        form = NegotiateForm()
        if form.validate_on_submit():
            try:
                rqst.n_amount = form.negotiate.data
                rqst.requested_by = roles[0]
                db.session.commit()
                return redirect(url_for('home.requests'))
            except Exception as e:
                db.session.rollback()
                flash(e)
        return render_template('uni/colab.html', form = form, page = 'Negotiate', roles = roles)
    flash('Request has been Accepted or Completed.')
    return redirect(url_for('home.requests'))

@home.route('/delete/rqst/<int:rqst_id>', methods = ['GET'])
@login_required
def delete_rqst(rqst_id):
    rqst = Requests.query.get(rqst_id)
    try:
        db.session.delete(rqst)
        db.session.commit()
        flash('Request Deleted')
    except Exception as e:
        db.session.rollback()
        flash(e)
    return redirect(url_for('home.requests'))

@home.route('/sponser/campaigns/<int:spn_id>', methods = ['GET', 'POST'])
@login_required
def spn_campaigns(spn_id):
    spn = Sponser.query.get(spn_id)
    campaigns = Campaign.query.filter_by(campaign_by = spn_id).order_by(decend(Campaign.start_date)).all()
    roles = user_roles(current_user.user_id)
    return render_template('uni/campaigns.html', user = spn, page = f'{spn.company_name}\'s Campaigns', roles = roles, campaigns = campaigns)

@home.route('/influencer/posts/<int:inf_id>', methods = ['GET', 'POST'])
@login_required
def inf_posts(inf_id):
    inf = Influencer.query.get(inf_id)
    posts = Posts.query.filter_by(post_by = inf_id).order_by(decend(Posts.post_id)).all()
    roles = user_roles(current_user.user_id)
    return render_template('uni/all_posts.html', user = inf, page = f'{inf.name}\'s Posts', roles = roles, posts = posts)

@home.route('/requests/accept/<int:rqst_id>', methods = ["GET", "POST"])
@login_required
def accept_rqst(rqst_id):
    roles = user_roles(current_user.user_id)
    rqst = Requests.query.get(rqst_id)
    if rqst.status == 'Accepted/Ongoing':
        flash('Already Accepted')
    elif rqst.campaign.end_date < datetime.utcnow():
        flash('Campaign for rqst has expired')
        return redirect(f'/delete/rqst/{rqst_id}')
    else:
        if roles[0] == rqst.requested_by:
            flash('You can\'t accept this Request as you Created it or Negotiated')
        else:
            try:
                rqst.status = 'Accepted/Ongoing'
                db.session.commit()
                flash('Accepted')
            except Exception as e:
                db.session.rollback()
                flash(e)
                return redirect(url_for('home.requests'))
    return redirect(url_for('home.requests'))        

@home.route('/wallet/add_balance', methods = ["GET", "POST"])
@login_required
def add_balance():
    form = PaymentForm()
    user = User.query.get_or_404(current_user.user_id)
    if form.validate_on_submit():
        if form.amount.data >= 10:
            if checkpw(form.password.data, user.password):
                try:
                    user.wallet_balance += form.amount.data
                    db.session.commit()
                    flash('Payment Successful!')
                    return redirect(f'/get/{current_user.user_id}')
                except Exception as e:
                    db.session.rollback()
                    flash(e)
            else:
                flash('Wrong Password, Try again.')
        else:
            flash('Amount must be alteast $10')
    return render_template('uni/pay.html', form = form)

@home.route('/like/<string:action>/<int:post_id>', methods = ["PUT"])
@login_required
def like_post(action, post_id):
    curr_user = User.query.get_or_404(current_user.user_id)
    post = Posts.query.get_or_404(post_id)

    like = LikedPost.query.get((curr_user.user_id, post.post_id))
    match action:
        case 'like':
            if like:
                return jsonify({'Request' : 'Post Already Liked'})
            else:
                try:
                    db.session.add(LikedPost(user_id = curr_user.user_id, post_id = post.post_id))
                    inf = Influencer.query.get(post.post_by)
                    inf.reach += 1
                    db.session.commit()
                    return jsonify({'Request' : 'liked'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'Request' : e})
        case 'dislike':
            if not like:
                return jsonify({'Request' : 'Post Already Dis-Liked'})
            try:
                db.session.delete(LikedPost.query.get((curr_user.user_id, post.post_id)))
                inf = Influencer.query.get(post.post_by)
                inf.reach -= 1
                db.session.commit()
                return jsonify({'Request' : 'disliked'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'Request' : e})
    
@home.route('/delete/account')
@login_required
def delete_account():
    user = User.query.get_or_404(current_user.user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Account Deleted')
        return redirect(url_for('home.landing_page'))
    except Exception as e:
        db.session.rollback()
        flash(e)
        return redirect(url_for('home.profile'))