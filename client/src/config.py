import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@postgres/flaskia'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key'
