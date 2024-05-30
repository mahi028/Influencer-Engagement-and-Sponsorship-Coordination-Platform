from flask import Blueprint, render_template, redirect, url_for, flash
from application import db
from application.modals import User, UserRoles, Influencer, Sponser
from application import login_manager
from application.form import RegisterForm, LoginForm, InfluencerDetailForm, SponserDetailForm, AdminLoginForm
from application.hash import hashpw, checkpw
from flask_login import login_required, login_user, logout_user, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_auth = Blueprint('user_auth', __name__)

@user_auth.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if not user:
            flash(f'No user found.')
        
        else:
            user_role = UserRoles.query.get((user.user_id, int(form.role.data)))

            if not user_role:
                roles = {1: 'Admin', 2: 'Influencer', 3: 'Sponser'}
                flash(f'No user found. Plese Register with role {roles[int(form.role.data)]} or create a new account.')

            elif not checkpw(form.password.data, user.password):
                flash('Wrong Password :( Please try again ')

            else:
                login_user(user)
                flash('Welcome :)')

                if int(form.role.data) == 1:
                    return redirect(url_for('home.dashboard'))
                
                elif int(form.role.data) == 2:
                    return redirect(url_for('user_auth.get_influencer_data'))

                elif int(form.role.data) == 3:
                    return redirect(url_for('user_auth.get_sponser_data'))
            
    return render_template('login.html', page = 'login',form = form)
    

@user_auth.route('/logout')
@login_required
def logout():
    flash('Logout Successful')
    logout_user()
    return redirect(url_for('user_auth.login'))


@user_auth.route('/register', methods = ["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user:
            if checkpw(form.password.data, user.password):
                user_role = UserRoles.query.get((user.user_id, int(form.role.data)))

                if user_role:
                    flash('Role already exists, Please Login')
                    return redirect(url_for("user_auth.login"))

                else:
                    try:
                        new_role = UserRoles(user_id = user.user_id, role_id = int(form.role.data))
                        db.session.add(new_role)
                        db.session.commit()
                        flash('New role has been created :)')
                        return redirect(url_for("user_auth.login"))                        

                    except Exception as e:
                        flash(e)
                        
            else:
                roles = {1: 'Admin', 2: 'Influencer', 3: 'Sponser'}
                flash(f'User exists, So plese type correct password to register as a {roles[int(form.role.data)]}. Or use another email.')

        else:
            if form.password.data == form.conf_password.data:
                try:
                    new_user = User(email = form.email.data, password = hashpw(form.password.data))
                    db.session.add(new_user)
                    db.session.commit()

                except Exception as e:
                    flash(e)

                else:
                    added_user = User.query.filter_by(email = form.email.data).first()

                    try:
                        new_role = UserRoles(user_id = added_user.user_id, role_id = int(form.role.data))
                        db.session.add(new_role)
                        db.session.commit()
                        flash('User created :)')
                        return redirect(url_for('user_auth.login'))
                    
                    except Exception as e:
                        db.session.delete(added_user)
                        db.session.commit()
                        flash(e)

            else:
                flash('Passwords did not match.')

    return render_template('register.html', page = 'register', form = form)
                        
@user_auth.route('/get_influencer_data', methods = ['GET', 'POST'])
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

@user_auth.route('/get_sponser_data', methods = ['GET', 'POST'])
@login_required
def get_sponser_data():
    if UserRoles.query.get((current_user.user_id, 3)):
        sponser = Sponser.query.get(current_user.user_id)

        if sponser:
            flash(f'Logged in as {sponser.name}')
            return redirect(url_for('home.dashboard'))
                
        form = SponserDetailForm()

        if form.validate_on_submit():
            try:
                new_sponser = Sponser(sponser_id = current_user.user_id, company_name = form.company_name.data, industry = form.industry.data, budget = int(form.budget.data))
                db.session.add(new_sponser)
                db.session.commit()
                flash('New Sponser account has been created :)')
                return redirect(url_for('home.dashboard'))

            except Exception as e:
                flash(e)

        return render_template('user_details.html', page = 'login', role = 'sponser', form = form)
        
    flash('Account with role Sponser does not exists. Try again')
    logout_user()
    return redirect(url_for('user_auth.login'))
    
@user_auth.route('/login/admin', methods = ['GET', 'POST'])
def adminLogin():
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        admin = User.query.filter_by(email = form.email.data).first()
        
        if admin:
            if checkpw(form.password.data, admin.password):
                role = UserRoles.query.get((admin.user_id, 1))
                
                if role:
                    login_user(admin)
                    flash('Logged in as Admin')
                    return redirect(url_for('home.dashboard'))
                else:
                    flash('You are not authorised to access this page')
                    return redirect(url_for('user_auth.login'))
            else:
                flash('Wrong Password')
        else:
            flash('No such user. Try Again')

    return render_template('login.html', page = 'Admin login',form = form)