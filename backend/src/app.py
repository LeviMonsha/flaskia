from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS
from src.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DATABASE_URL, JWT_KEY

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_KEY

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Имя пользователя и пароль обязательны'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Пользователь уже существует'}), 400

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Пользователь успешно зарегистрирован', 'username': username, 'title': 'Добро пожаловать'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Произошла ошибка при регистрации пользователя', 'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        access_token = create_access_token(identity=username)
        return jsonify({'message': 'Успешный вход', 'username': username, 'title': 'Добро пожаловать'}), 200
    else:
        return jsonify({'message': 'Неправильный логин или пароль'}), 401

@app.route('/')
@jwt_required()
def index():
    return jsonify({'message': 'Привет! Вы авторизованы.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
