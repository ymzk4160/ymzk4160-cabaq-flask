from datetime import datetime
from app.extensions import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    target_type = db.Column(db.String(20))
    target_id = db.Column(db.Integer)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    is_emailed = db.Column(db.Boolean, default=False)
    is_push_sent = db.Column(db.Boolean, default=False)
    is_line_sent = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('notifications', lazy=True))
    from_user = db.relationship('User', foreign_keys=[from_user_id]) 
