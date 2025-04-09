from flask import Blueprint, render_template
from flask_login import current_user

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template('home.html', title='Главная страница', user=current_user)
