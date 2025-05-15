from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from src.forms import RegistrationForm, LoginForm
from src.models import User
from src.db import db

auth = Blueprint('auth', __name__)

@auth.route('/registration', methods=['GET', 'POST'])
def registration_page():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    
    register_form = RegistrationForm()

    if register_form.submit.data and register_form.validate_on_submit():
        user = User.query.filter_by(username=register_form.username.data).first()
        if user:
            flash('Пользователь уже существует')
            return render_template('registration.html', register_form=register_form)
        
        new_user = User(username=register_form.username.data, email=register_form.email.data)
        new_user.set_password(register_form.password.data)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home.home_page'))
    
    return render_template('registration.html', register_form=register_form)

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home.home_page'))
    
    login_form = LoginForm()

    if login_form.submit.data and login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('home.home_page'))
        else:
            flash('Неправильный логин или пароль')
            return render_template('login.html', login_form=login_form)

    return render_template('login.html', login_form=login_form)
