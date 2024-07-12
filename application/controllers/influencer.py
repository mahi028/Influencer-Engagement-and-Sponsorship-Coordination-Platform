from flask import Blueprint, render_template, jsonify, redirect, url_for, flash
from application import db
from application.modals import UserRoles, Influencer, Requests, Campaign, User
from application.form import InfluencerDetailForm
from flask_login import login_required, current_user

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

        
# @influencer.route('/negotiate/<int:camp_id>', methods = ["GET", 'POST'])
# @login_required
# def negotiate(camp_id):
#     camp = Campaign.query.get(camp_id)
#     curr_user = User.query.get(current_user.user_id)

#     form  = NegotiateForm()
#     if form.validate_on_submit():
#         try:
#             camp.n_amount = form.budget.data
#             db.session.commit()
#             return redirect(url_for('home.requests'))
#         except Exception as e:
#             flash(e)
#     return render_template('negotiate.html', form = form)
    