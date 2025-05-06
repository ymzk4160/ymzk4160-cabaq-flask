from datetime import datetime
from app.extensions import db
from sqlalchemy.orm import relationship
from app.models.user import User  # 追加：Userモデルをインポート

class Question(db.Model):
    __tablename__ = 'questions'  # 修正：**tablename**→__tablename__
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))  # 修正：categoryをcategory_idに変更
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外部キー
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # リレーションシップ
    user = relationship("User", foreign_keys=[user_id], backref="questions")  # 修正：back_populates→backref
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    category = relationship("Category", foreign_keys=[category_id])  # 追加：categoryリレーションシップ
    
    def __repr__(self):  # 修正：**repr**→__repr__
        return f'<Question {self.id}: {self.title}>'
