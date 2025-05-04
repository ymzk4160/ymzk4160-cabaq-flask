# app/models/__init__.py

# モデルを明示的にインポートして二重登録を防ぐ
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer

__all__ = ['User', 'Question', 'Answer']
