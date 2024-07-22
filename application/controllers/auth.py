from flask import Blueprint, render_template, redirect, url_for, flash, request
from application import db
from application.modals import User, UserRoles
from application import login_manager
from application.form import RegisterForm, LoginForm
from application.hash import hashpw, checkpw
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from uuid import uuid4

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
            if checkpw(form.password.data, user.password):
                login_user(user)
                user.active_flag = True
                db.session.commit()
                flash('Welcome :)')

                return redirect(url_for('home.dashboard'))

            else:
                flash('Wrong Password :( Please try again ')
            
    return render_template('auth/login.html', page = 'login',form = form)
    

@user_auth.route('/logout')
@login_required
def logout():
    user = User.query.get(current_user.user_id)
    logout_user()
    user.active_flag = False
    db.session.commit()
    flash('Logout Successful')
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
                    new_user = User(email = form.email.data, password = hashpw(form.password.data), profile = new_image_name)
                    db.session.add(new_user)
                    db.session.commit()
                    if image_file:
                        image_file.save(image_path) 


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

    return render_template('auth/register.html', page = 'register', form = form)
 
@user_auth.route('/login/admin', methods = ['GET', 'POST'])
def adminLogin():
    form = LoginForm()
    
    if form.validate_on_submit():
        admin = User.query.filter_by(email = form.email.data).first()
        
        if admin:
            if checkpw(form.password.data, admin.password):
                role = UserRoles.query.get((admin.user_id, 1))
                
                if role:
                    login_user(admin)
                    admin.active_flag = True
                    db.session.commit()
                    flash('Logged in as Admin')
                    return redirect(url_for('home.dashboard'))
                else:
                    flash('You are not authorised to access this page')
                    return redirect(url_for('user_auth.login'))
            else:
                flash('Wrong Password')
        else:
            flash('No such user. Try Again')

    return render_template('auth/login.html', page = 'Admin Login',form = form)