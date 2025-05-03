from datetime import datetime
from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外部キー
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # リレーションシップ
    user = relationship("app.models.user.User", back_populates="questions")
    answers = relationship("app.models.answer.Answer", back_populates="question")
    
    def __repr__(self):
        return f'<Question {self.id}: {self.title}>'
