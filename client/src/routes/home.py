from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, logout_user

from ..forms import PostForm
from ..models import Post
from ..db import db

home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def home_page():
    post_form = PostForm()
    
    if current_user.is_authenticated & post_form.validate_on_submit():
        post = Post(
            title=post_form.title.data,
            body=post_form.body.data,
            author=current_user._get_current_object()
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home.home_page'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('home.html', 
                         post_form=post_form,
                         posts=posts,
                         user=current_user)

@home.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home.home_page'))