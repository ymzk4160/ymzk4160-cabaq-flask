from datetime import datetime
# from flask_login import UserMixin  # コメントアウト
from sqlalchemy.dialects.postgresql import JSON
from app.extensions import db  # login_managerを削除

# @login_manager.user_loader  # コメントアウト
# def load_user(user_id):     # コメントアウト
#     return User.query.get(int(user_id))  # コメントアウト

class User(db.Model):  # UserMixinを削除
    # 既存のコード...
