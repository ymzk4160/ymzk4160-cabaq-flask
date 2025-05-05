from flask import Blueprint, render_template
from app.extensions import db
from app.models.question import Question

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    try:
        # データベースから質問を取得するシンプルな実装
        questions = []
        db_questions = Question.query.order_by(Question.created_at.desc()).limit(10).all()
        
        for q in db_questions:
            category_name = q.category.name if q.category else "未分類"
            
            questions.append({
                'id': q.id,
                'title': q.title,
                'content': q.content,
                'category': category_name,
                'answer_count': len(q.answers) if hasattr(q, 'answers') else 0,
                'answers': [{'content': a.content} for a in q.answers] if hasattr(q, 'answers') else []
            })
            
        return render_template('main/index.html', questions=questions)
    except Exception as e:
        return f"データベースエラー: {str(e)}"
