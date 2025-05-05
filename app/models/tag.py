from datetime import datetime
from app.extensions import db

class QuestionTag(db.Model):
    __tablename__ = 'question_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    question = db.relationship('Question', backref=db.backref('question_tags', lazy=True))
    tag = db.relationship('Tag', backref=db.backref('question_tags', lazy=True))
