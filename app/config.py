import os
from datetime import timedelta

# 基本設定
DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_for_development')

# データベース設定
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# セッション設定
PERMANENT_SESSION_LIFETIME = timedelta(days=30)
