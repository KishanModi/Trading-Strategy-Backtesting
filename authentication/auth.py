from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_jwt_extended import jwt_required, create_access_token
from .models import User
from .app import db, mail
import os

auth = Blueprint('auth', __name__)

#### Routes ####

#sign up route
@auth.route('/signup')
def signup():
  return render_template('signup.html')

#sign up route when user post their details to server
@auth.route('/signup', methods=['POST'])
def signup_post():
  username = request.form.get('username')
  email = request.form.get('email')
  password = request.form.get('password')

  #check if user's email is in database or not
  user = User.query.filter_by(email = email).first()
  if user:
    flash('Email address already exists')
    return redirect(url_for('auth.signup'))

  #if not create new user
  new_user = User(username = username, email = email, password = generate_password_hash(password, method='sha256'))

  db.session.add(new_user)
  db.session.commit()

  return redirect(url_for('auth.login'))


#login route when user is not logged in
@auth.route('/login')
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.profile'))
  return render_template('login.html')

#login route when user post login details to the server
@auth.route('/login', methods=['POST'])
def login_post():
  email = request.form.get('email')
  password = request.form.get('password')
  remember = True if request.form.get('remember') else False

  #check if user is in database or not
  user = User.query.filter_by(email=email).first()

  #check password and user
  if not user or not check_password_hash(user.password, password):
    flash('Please check your login details and try again.', 'danger')
    return redirect(url_for('auth.login'))

  #redirect user to profile page
  login_user(user, remember=remember)
  return redirect(url_for('main.profile'))


#route for forgot password page
@auth.route('/forgot', methods=['GET','POST'])
def forgot():
  if request.method == "GET":
    return render_template('forgot.html')

  if request.method == "POST":
    email = request.form.get('email')
    user = User.verify_email(email)

    if user:
      send_email(user)
      flash('An email has been sent with instructions to reset your password.', 'info')
      return redirect(url_for('auth.login'))
    else:
      flash('Please Enter A Valid Email', 'danger')
      return redirect(url_for('auth.forgot'))


#route for resetting password
@auth.route('/reset/<token>', methods = ['GET', 'POST'])
def reset_verified(token):
  user = User.verify_reset_token(token)

  if not user:
    flash('User not found or token has expired', 'warning')
    return redirect(url_for('auth.reset'))

  password = request.form.get('password')
  if len(password or ()) < 8:
    flash('Your password needs to be at least 8 characters', 'error')
  if password:
    hashed_password = generate_password_hash(password, method='sha256')
    user.password = hashed_password

    db.session.commit()
    flash('Your password has been updated! You are now able to log in', 'success')
    return redirect(url_for('auth.login'))
  return render_template('reset.html')


#logout route
@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))


#fuction that sends email for password reset to user's email id from sendgrid smtp server with secret token
def send_email(user):
  token = user.get_reset_token()
  msg = Message()
  msg.subject = "Login System: Password Reset Request"
  #msg.sender = ''
  msg.recipients = [user.email]
  msg.html = render_template('reset_pwd.html', user = user, token = token)
  mail.send(msg)
