from datetime import datetime
from app.extensions import db

class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    awarded_at = db.Column(db.DateTime, server_default=db.func.now())
    awarded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_displayed = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('badges', lazy=True))
    badge = db.relationship('Badge', backref=db.backref('users', lazy=True))
    awarder = db.relationship('User', foreign_keys=[awarded_by])
