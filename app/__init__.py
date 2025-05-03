from flask import Flask, render_template
from app.extensions import db, migrate, bcrypt  # login_managerを削除

def create_app():
    app = Flask(__name__)
    
    # 設定読み込み
    app.config.from_object('app.config')
    
    # 拡張機能の初期化
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    # login_manager.init_app(app)  # コメントアウト
    
    # ブループリントの登録
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # 認証ブループリントの登録をコメントアウト
    # from app.routes.auth import bp as auth_bp
    # app.register_blueprint(auth_bp)
    
    # エラーハンドラー
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    return app
