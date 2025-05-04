from flask import Flask, render_template
from app.routes import main
from app.extensions import db

def create_app():
    app = Flask(__name__)
    
    # データベース設定
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # SQLAlchemyの初期化
    db.init_app(app)
    
    # Blueprintを登録
    app.register_blueprint(main.bp)
    
    # 404エラーハンドラー
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    return app
