from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

home = Blueprint('home',__name__)

@home.route('/')
def index():
    return 'hello'

@home.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')