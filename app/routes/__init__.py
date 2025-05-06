from flask import Flask, render_template
from app.extensions import db

def create_app():
    app = Flask(__name__)
    
    # データベース設定
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # SQLAlchemyの初期化
    db.init_app(app)
    
    # モデルのインポート（順序が重要）
    from app.models.user import User
    from app.models.category import Category
    from app.models.question import Question
    from app.models.answer import Answer
    
    # Blueprintを登録
    from app.routes import main
    app.register_blueprint(main.bp)
    
    # データ管理用ブループリント登録
    from app.routes.data import bp as data_bp
    app.register_blueprint(data_bp)
    
    # 404エラーハンドラー
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    # データベース作成
    with app.app_context():
        db.create_all()
    
    return app
