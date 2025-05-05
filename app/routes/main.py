from flask import Blueprint, render_template
from app.models.question import Question
from app.models.answer import Answer
from app.models.category import Category

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    # データベースから質問を取得
    questions = Question.query.order_by(Question.created_at.desc()).limit(10).all()
    return render_template('main/index.html', questions=questions)
