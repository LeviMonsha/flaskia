from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, logout_user

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('home.html', user=current_user, posts=posts)

@home.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home.home_page'))