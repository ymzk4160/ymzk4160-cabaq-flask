from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager  # コメントアウト

# データベース
db = SQLAlchemy()
# マイグレーション
migrate = Migrate()
# パスワードハッシュ化
bcrypt = Bcrypt()
# ログイン管理（すべてコメントアウト）
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.login_message = 'この機能を使用するにはログインが必要です。'
# login_manager.login_message_category = 'info'
