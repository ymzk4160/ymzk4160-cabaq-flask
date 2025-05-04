from datetime import datetime
from app.extensions import db
from sqlalchemy.orm import relationship

class Answer(db.Model):
    __tablename__ = 'answers'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外部キー
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # リレーションシップ（完全修飾パスを使用）
    question = relationship("app.models.question.Question", back_populates="answers")
    user = relationship("app.models.user.User", back_populates="answers")
    
    def __repr__(self):
        return f'<Answer {self.id} for Question {self.question_id}>'
