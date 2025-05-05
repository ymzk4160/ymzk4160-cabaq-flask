from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# 他のインポート

# データベースオブジェクトを作成
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # アプリケーション設定
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'  # 実際の接続URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # データベースを初期化
    db.init_app(app)
    
    # ここでモデルをインポート（循環インポートを避けるため、関数内でインポート）
    # これが重要な部分です！
    from app.models.user import User
    from app.models.question import Question
    from app.models.answer import Answer
    from app.models.category import Category
    # その他必要なモデルをすべてインポート
    
    # ブループリントを登録
    from app.routes import main
    app.register_blueprint(main.bp)
    
    return app
