from flask import Blueprint, render_template, redirect, url_for
# from flask_login import current_user  # コメントアウト
from app.extensions import db
from datetime import datetime

# Blueprintを作成
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    # 固定ダミーデータを直接作成
    recent_questions = [
        {
            'id': 1,
            'title': '初めてのキャバクラ勤務、何から準備すれば？',
            'category': '初心者',
            'created_at': datetime.utcnow(),
            'answer_count': 2,
            'answers': [{'content': 'ドレスは最初は2〜3着あれば十分です！私は最初、古着屋で手頃な値段のものを買いました。'}]
        },
        # 他のダミーデータ...
    ]
    
    return render_template('main/index.html', questions=recent_questions)
