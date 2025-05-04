from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from datetime import datetime, timedelta
import random
from app.models import User, Question, Answer

# まず最初にBlueprintを作成
bp = Blueprint('main', __name__, url_prefix='')

@bp.route('/')
def index():
    """トップページ"""
    # データベースから最新の質問を取得
    try:
        recent_questions = Question.query.filter_by(is_deleted=False).order_by(Question.created_at.desc()).limit(10).all()
    except Exception as e:
        print(f"エラー発生: {str(e)}")
        recent_questions = []
    
    return render_template('main/index.html', questions=recent_questions)

# 以下、その他のルート定義...
