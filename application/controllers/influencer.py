from flask import Blueprint, render_template, redirect, url_for, flash
from application import db
from application.modals import User, UserRoles, Influencer, Sponser
from application.form import RegisterForm, LoginForm, InfluencerDetailForm, SponserDetailForm, AdminLoginForm
from application.hash import hashpw, checkpw
from flask_login import login_required, login_user, logout_user, current_user


influencer = Blueprint('influencer', __name__)

                       
@influencer.route('/get_influencer_data', methods = ['GET', 'POST'])
@login_required
def get_influencer_data():
    if UserRoles.query.get((current_user.user_id, 2)):
        inf = Influencer.query.get(current_user.user_id)

        if inf:
            flash(f'Logged in as {inf.name}')
            return redirect(url_for('home.dashboard'))
        
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
        
    flash('Account with role Inluencer does not exists. Try again')
    logout_user()
    return redirect(url_for('user_auth.login'))