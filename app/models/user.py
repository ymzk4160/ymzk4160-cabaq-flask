from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(80), nullable=False)
    display_name = db.Column(db.String(80))
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='active')  # active, inactive, banned
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーションシップ（完全修飾パスを使用）
    user_questions = relationship("app.models.question.Question", back_populates="user")
    answers = relationship("app.models.answer.Answer", back_populates="user")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.nickname}>'
