from datetime import datetime
from app.extensions import db

class Question(db.Model):
    __tablename__ = 'questions'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    # 関連情報
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # システム情報
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーションシップ
    answers = db.relationship('Answer', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Question {self.title}>'
    
    @property
    def answer_count(self):
        return self.answers.filter_by(is_deleted=False).count()

class Answer(db.Model):
    __tablename__ = 'answers'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    
    # 関連情報
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # システム情報
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    def __repr__(self):
        return f'<Answer {self.id} for Question {self.question_id}>'
