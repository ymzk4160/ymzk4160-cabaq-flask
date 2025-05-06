from datetime import datetime
from app.extensions import db
from sqlalchemy.orm import relationship

class Question(db.Model):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外部キー
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # リレーションシップをシンプルに定義
    user = db.relationship('User', backref=db.backref('questions', lazy='dynamic'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    category = db.relationship('Category', backref=db.backref('questions', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Question {self.id}: {self.title}>'
