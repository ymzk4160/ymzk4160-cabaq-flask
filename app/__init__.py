from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# データベースオブジェクトの作成
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # データベースの初期化
    db.init_app(app)
    
    # すべてのモデルをインポート
    from app.models.user import User
    from app.models.question import Question
    from app.models.answer import Answer
    from app.models.category import Category
    from app.models.answer_comment import AnswerComment
    from app.models.tag import Tag
    from app.models.question_tag import QuestionTag
    from app.models.reaction import Reaction
    from app.models.notification import Notification
    from app.models.payment import Payment
    from app.models.payment_history import PaymentHistory
    from app.models.report import Report
    from app.models.view import View
    from app.models.badge import Badge
    from app.models.user_badge import UserBadge
    from app.models.setting import Setting
    
    # ブループリントの登録
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app
