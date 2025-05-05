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
    
    # データ管理用ブループリント登録
    from app.routes.data import bp as data_bp
    app.register_blueprint(data_bp)
    
    # 以下の存在しないブループリントは一時的にコメントアウト
    # from app.routes.auth import bp as auth_bp
    # app.register_blueprint(auth_bp)
    
    # from app.routes.admin import bp as admin_bp
    # app.register_blueprint(admin_bp)
    
    # from app.routes.user import bp as user_bp
    # app.register_blueprint(user_bp)
    
    # from app.routes.question import bp as question_bp
    # app.register_blueprint(question_bp)
    
    # from app.routes.answer import bp as answer_bp
    # app.register_blueprint(answer_bp)
    
    # from app.routes.comment import bp as comment_bp
    # app.register_blueprint(comment_bp)
    
    # from app.routes.search import bp as search_bp
    # app.register_blueprint(search_bp)
    
    # from app.routes.notification import bp as notification_bp
    # app.register_blueprint(notification_bp)
    
    # from app.routes.payment import bp as payment_bp
    # app.register_blueprint(payment_bp)
    
    # from app.routes.message import bp as message_bp
    # app.register_blueprint(message_bp)
    
    return app
