from datetime import datetime
from app.extensions import db

class AnswerComment(db.Model):
    __tablename__ = 'answer_comments'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    
    # ツリー構造管理
    parent_id = db.Column(db.Integer, db.ForeignKey('answer_comments.id'))
    reply_depth = db.Column(db.Integer, default=0)
    original_answer_id = db.Column(db.Integer)
    first_reply_user_id = db.Column(db.Integer)
    
    # 状態/統計情報
    is_anonymous = db.Column(db.Boolean, default=False)
    reaction_count = db.Column(db.Integer, default=0)
    edit_count = db.Column(db.Integer, default=0)
    
    # メディア情報
    has_images = db.Column(db.Boolean, default=False)
    images = db.Column(db.JSON)
    
    # 管理/メタ情報
    last_edited_at = db.Column(db.DateTime)
    ip_address = db.Column(db.String(45))
    remarks = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    deleted_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    answer = db.relationship('Answer', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('answer_comments', lazy=True))
    replies = db.relationship('AnswerComment', backref=db.backref('parent_comment', remote_side=[id]))
