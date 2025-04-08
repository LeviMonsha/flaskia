from flask import Blueprint, render_template, redirect, url_for, flash
from src.forms import RegistrationForm, LoginForm
from src.models import User

auth = Blueprint('auth', __name__)

@auth.route('/auth', methods=['GET', 'POST'])
def auth_page():
    register_form = RegistrationForm()
    login_form = LoginForm()

    if register_form.submit.data and register_form.validate_on_submit():
        user = User.query.filter_by(username=register_form.username.data).first()
        if user:
            return render_template('auth.html', register_form=register_form, login_form=login_form, message='Пользователь уже существует')
        
        new_user = User(username=register_form.username.data, password=register_form.password.data)
        from src.db import db
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home.home_page'))

    if login_form.submit.data and login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.password == login_form.password.data:
            return redirect(url_for('home.home_page'))
        else:
            return render_template('auth.html', register_form=register_form, login_form=login_form, message='Неправильный логин или пароль')

    return render_template('auth.html', register_form=register_form, login_form=login_form)
