import os
from flask import Flask
from app.extensions import db, migrate, bcrypt, login_manager
from app.config import config

def create_app(config_name='default'):
    """アプリケーションファクトリー関数"""
    app = Flask(__name__)
    
    # 設定読み込み
    app.config.from_object(config[config_name])
    
    # 拡張機能の初期化
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # ルートの登録
    from app.routes import main
    app.register_blueprint(main.bp)
    
    return app