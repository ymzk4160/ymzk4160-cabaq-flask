from datetime import datetime
from app.extensions import db

class View(db.Model):
    __tablename__ = 'views'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    session_id = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    referrer = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('views', lazy=True))
    question = db.relationship('Question', backref=db.backref('views', lazy=True))
