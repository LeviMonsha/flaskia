from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from src.config import Config
from src.db import db

csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__,
            static_folder='../static',
            template_folder='../templates')
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)

    from src.routes.auth import auth
    from src.routes.home import home

    app.register_blueprint(auth)
    app.register_blueprint(home)

    with app.app_context():
        db.create_all()

    return app
