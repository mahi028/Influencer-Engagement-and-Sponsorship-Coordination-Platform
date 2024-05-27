from flask import Blueprint, request, render_template, redirect, url_for, flash
from application import db
from application.modals import User, Role, UserRoles
from application import login_manager
from application.form import RegisterForm, LoginForm, InfluencerDetailForm, SponserDetailForm
from application.hash import hashpw, checkpw
from flask_login import login_required, login_user, logout_user, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_auth = Blueprint('user_auth', __name__)

@user_auth.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'GET':
        
        return render_template('login.html', form = form)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if not user:
                flash(f'No user found.')
                return redirect(url_for('user_auth.register'))
            elif not checkpw(form.password.data, user.password):
                flash('Wrong Password :(. Please try again ')
                return redirect(url_for('user_auth.login'))
            else:
                user_role = UserRoles.query.get((user.user_id, int(form.role.data)))
                if not user_role:
                    roles = {1: 'Admin', 2: 'Influencer', 3: 'Sponser'}
                    flash(f'No user found. Plese Register with role {roles[int(form.role.data)]} or create a new account.')
                    return redirect(url_for('user_auth.register'))
                login_user(user)
                flash('Welcome :)')
                return redirect(url_for('home.dashboard'))

@user_auth.route('/logout')
@login_required
def logout():
    flash('Logout Successful')
    logout_user()
    return redirect(url_for('user_auth.logout'))


@user_auth.route('/register', methods = ["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'GET':

        return render_template('register.html',form = form)
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user:
                if checkpw(form.password.data, user.password):
                    user_role = UserRoles.query.get((user.user_id, int(form.role.data)))
                    if user_role:
                        flash('Role already exists, Please Login')
                    else:
                        new_role = UserRoles(user_id = user.user_id, role_id = form.role.data)
                        db.session.add(new_role)
                        db.session.commit()
                        flash('New role has been created :)')
                    return redirect(url_for("user_auth.login"))
                else:
                    roles = {1: 'Admin', 2: 'Influencer', 3: 'Sponser'}
                    flash(f'User exists, So plese type correct password to register as a {roles[int(form.role.data)]}.<br>Or use another email.')
                    return redirect(url_for("user_auth.register"))

            else:
                if form.password.data == form.conf_password.data:
                    try:
                        new_user = User(email = form.email.data, password = hashpw(form.password.data))
                        db.session.add(new_user)
                        db.session.commit()
                    except Exception as e:
                        flash(e)
                        return redirect(url_for("user_auth.register"))
                    else:
                        added_user = User.query.filter_by(email = form.email.data).first()
                        try:
                            new_role = UserRoles(user_id = added_user.user_id, role_id = form.role.data)
                            db.session.add(new_role)
                            db.session.commit()
                        except Exception as e:
                            db.session.delete(added_user)
                            db.session.commit()
                            flash(e)
                            return redirect(url_for("user_auth.register"))
                        else:
                            flash('User created :)')
                            return redirect(url_for('user_auth.login'))