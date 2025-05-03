from datetime import datetime
from app.extensions import db
from sqlalchemy.orm import relationship

class Question(db.Model):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}  # 既存テーブル再定義を許可
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外部キー
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # シンプルなリレーションシップ定義
    user = relationship("User", foreign_keys=[user_id])
    answers = relationship("Answer")
    
    def __repr__(self):
        return f'<Question {self.id}: {self.title}>'
