from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .app import db

main = Blueprint('main', __name__)

#index route
@main.route('/')
def index():
  return render_template('index.html')

@main.route('/dashboard')
def dashboard():
  return render_template('dashboard.html')

#profile page route
@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', name=current_user.username)
