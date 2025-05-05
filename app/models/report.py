from datetime import datetime
from app.extensions import db

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_type = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    reason_type = db.Column(db.String(50))
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(20), default='medium')
    handled_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    action_taken = db.Column(db.String(255))
    internal_notes = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('reports', lazy=True))
    handler = db.relationship('User', foreign_keys=[handled_by])
