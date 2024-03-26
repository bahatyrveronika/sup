from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.file import  FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfilly!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.main'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exists', category='error')
    return render_template('entry.html', user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.main'))

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(username)<4:
            flash('The name must be at least 3 characters long')
        else:
            new_user = User(email=email, name=username, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.main'))
    return render_template('entry.html', user = current_user)

def valid_pass(password):
    if len(password)<=7:
        return False
    for i in password:
        if i==' ':
            return False
    for i in password:
        if i.isdigit():
            return True
        
# class AccountUpdateForm(FlaskForm):
#     picture = FileField(label = 'Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
#     submit = SubmitField(label='Update Account')
        
# @auth.route('/photo')
# def account():
#     image_file = url_for('static', filename = 'profile_pics/'+ current_user.image_file)
#     return render_template('account.html', image_file = image_file)
        

# @auth.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', user=current_user)