from flask import Flask
from app.extensions import db
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # データベースの初期化
    db.init_app(app)
    
    # アプリコンテキストをグローバルにプッシュ
    app.app_context().push()
    
    # モデルのインポート（循環インポートを避けるためここでインポート）
    from app.models import user, question, answer, category, answer_comment, tag
    from app.models import question_tag, reaction, notification, payment, payment_history
    from app.models import report, view, badge, user_badge, setting
    
    # ブループリントの登録
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # 他のブループリントも登録
    
    return app
