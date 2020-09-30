from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from ..models import User
# from .forms import  LoginForm,RegistrationForm
from .. import db
from ..email import mail_message


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    email = request.form.get('email')
    username = request.form.get('username')
    password_hash = request.form.get('password_hash')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name, password=generate_password_hash(password_hash, method='collo254'))

    db.session.add(user)
    db.session.commit()
    mail_message("Welcome to HackerRank", "email/welcome_user",
                        user.email, new_user=new_user)

    return redirect(url_for('auth.login'))
    return render_template('auth/signup.html')

@ auth.route('/login', methods=['GET', 'POST'])
def login():
    email=request.form.get('email')
    password_hash=request.form.get('password_hash')
    remember=True if request.form.get('remember') else False

    user=User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password_hash):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@ auth.route('/logout')
@ login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

