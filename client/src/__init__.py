from flask import Flask
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from src.config import Config
from src.models import User
from src.db import db
from src.routes.auth import auth
from src.routes.home import home

csrf = CSRFProtect()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__,
                static_folder='../static',
                template_folder='../templates')
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(home)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()

    return app
