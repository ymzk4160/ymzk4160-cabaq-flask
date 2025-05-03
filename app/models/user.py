from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON
from app.extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.Text)
    login_type = db.Column(db.String(20))
    google_id = db.Column(db.String(255))
    line_id = db.Column(db.String(255))

    # 表示/プロフィール情報
    nickname = db.Column(db.String(50), unique=True)
    display_name = db.Column(db.String(50))
    avatar_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    birthday = db.Column(db.Date)
    age = db.Column(db.Integer)

    # システム設定/管理情報
    is_paid = db.Column(db.Boolean, default=False)
    trial_end_date = db.Column(db.DateTime)
    role = db.Column(db.String(20), default='user')
    status = db.Column(db.String(20), default='active')
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<User {self.nickname}>'

    def set_password(self, password):
        """パスワードをハッシュ化して保存"""
        from app.extensions import bcrypt
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """パスワードを検証"""
        from app.extensions import bcrypt
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_admin(self):
        """管理者かどうか"""
        return self.role == 'admin'
