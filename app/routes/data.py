from flask import Blueprint, jsonify
from app.extensions import db
from app.models import User, Question, Category  # 必要なモデルをインポート

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/db-check')
def db_check():
    try:
        users = User.query.all()
        questions = Question.query.all()
        categories = Category.query.all()

        return jsonify({
            'users': len(users),
            'questions': len(questions),
            'categories': len(categories)
        })
    except Exception as e:
        return jsonify({'error': str(e)})
