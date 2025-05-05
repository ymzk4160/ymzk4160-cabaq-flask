from datetime import datetime
from app.extensions import db

class Reaction(db.Model):
    __tablename__ = 'reactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_type = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    reaction_type = db.Column(db.String(20), nullable=False)
    is_visible = db.Column(db.Boolean, default=True)
    ip_address = db.Column(db.String(45))
    remarks = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('reactions', lazy=True)) 
