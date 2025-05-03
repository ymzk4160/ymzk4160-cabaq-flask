from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from app.extensions import db

class Question(db.Model):
    __tablename__ = 'questions'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # カテゴリ関連
    category = db.Column(db.String(50))
    
    # 状態管理
    is_solved = db.Column(db.Boolean, default=False)
    best_answer_id = db.Column(db.Integer)
    is_public = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    
    # 統計情報
    view_count = db.Column(db.Integer, default=0)
    answer_count = db.Column(db.Integer, default=0)
    
    # 管理/メタ情報
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('questions', lazy=True))
    
    def __repr__(self):
        return f'<Question {self.id}: {self.title[:20]}>'

class Answer(db.Model):
    __tablename__ = 'answers'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    
    # 状態管理
    is_best_answer = db.Column(db.Boolean, default=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    
    # 管理/メタ情報
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))
    user = db.relationship('User', backref=db.backref('answers', lazy=True))
    
    def __repr__(self):
        return f'<Answer {self.id} for Question {self.question_id}>'