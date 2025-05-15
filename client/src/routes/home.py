from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user, logout_user

from ..forms import PostForm
from ..models import Post
from ..db import db
from ..models import User, Post

home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def home_page():
    post_form = PostForm()
    user_followed = []
    user_followers = []

    if current_user.is_authenticated:
        user_followed = current_user.followed.all()
        user_followers = current_user.followers.all()
        if post_form.validate_on_submit():
        
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
                        user_followed=user_followed,
                        user_followers=user_followers,
                        user=current_user)

@home.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home.home_page'))


@home.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@home.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@home.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data:
        return jsonify({'error': 'Ошибка создания пользователя'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@home.route('/users/<int:user_id>/follow/<int:follow_id>', methods=['POST'])
def follow_user(user_id, follow_id):
    user = User.query.get_or_404(user_id)
    to_follow = User.query.get_or_404(follow_id)
    if user.id == to_follow.id:
        return jsonify({'error': 'Нельзя подписаться на самого себя'}), 400
    user.follow(to_follow)
    db.session.commit()
    return jsonify({'message': f'{user.username} подписался на {to_follow.username}'}), 200

@home.route('/users/<int:user_id>/unfollow/<int:unfollow_id>', methods=['POST'])
def unfollow_user(user_id, unfollow_id):
    user = User.query.get_or_404(user_id)
    to_unfollow = User.query.get_or_404(unfollow_id)
    user.unfollow(to_unfollow)
    db.session.commit()
    return jsonify({'message': f'Вы отписались от {to_unfollow.username}'}), 200

@home.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    if not data or not all(k in data for k in ('title', 'body', 'user_id')):
        return jsonify({'error': 'Не удалось создать пост'}), 400
    
    user = User.query.get_or_404(data['user_id'])
    post = Post(title=data['title'], body=data['body'], author=user)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201
