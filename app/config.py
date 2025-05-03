import os
from datetime import timedelta

class Config:
    """共通設定"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///cabaq.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # セッション設定
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    
    # 画像アップロード
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True

class TestingConfig(Config):
    """テスト環境設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """本番環境設定"""
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # 本番環境向けの設定を追加
        import logging
        from logging.handlers import RotatingFileHandler
        
        handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)

# 環境設定の辞書
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 