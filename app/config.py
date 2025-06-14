import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 0)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret')
