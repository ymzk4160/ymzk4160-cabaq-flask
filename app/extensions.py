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

# ログイン管理
# login_manager = LoginManager()  # コメントアウト
# login_manager.login_view = 'auth.login'  # コメントアウト
# login_manager.login_message = 'この機能を使用するにはログインが必要です。'  # コメントアウト
# login_manager.login_message_category = 'info'  # コメントアウト
