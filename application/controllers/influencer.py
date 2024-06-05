from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request
from application import db
from application.modals import User, UserRoles, Influencer, Sponser, Requests, Campaign
from application.form import RegisterForm, LoginForm, InfluencerDetailForm, SponserDetailForm, AdminLoginForm
from application.hash import hashpw, checkpw
from flask_login import login_required, login_user, logout_user, current_user


influencer = Blueprint('influencer', __name__)

                       
@influencer.route('/get_influencer_data', methods = ['GET', 'POST'])
@login_required
def get_influencer_data():
    form = InfluencerDetailForm()

    if form.validate_on_submit():
        try:
            new_inf = Influencer(influencer_id = current_user.user_id, name = form.name.data, category = form.category.data, niche = form.niche.data)
            db.session.add(new_inf)
            db.session.commit()
            flash('Influencer account has been created :)')
            return redirect(url_for('home.dashboard'))

        except Exception as e:
            flash(e)

    return render_template('user_details.html', page = 'login', role = 'influencer', form = form)

@influencer.route('/colab/<int:campaign_id>', methods = ['POST'])
@login_required
def colab(campaign_id):
    campaign_id = int(campaign_id)
    campaign = Campaign.query.get(campaign_id)
    if campaign.campaign_by != current_user.user_id:
        rqst = Requests.query.filter_by(campaign_id = campaign_id, influencer_id = current_user.user_id).first()
        if not rqst:
            try:
                new_rqst = Requests(campaign_id = campaign_id, influencer_id = current_user.user_id)
                db.session.add(new_rqst)
                db.session.commit()
                return jsonify({'Request': 'Success'})
            except Exception as e:
                print(e)
                return jsonify({'Request': 'Failed'})
        return jsonify({'Request': 'Already Exist'})
    return jsonify({'Request': 'Can\'t colab with self.'})