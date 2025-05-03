from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from app.models.question import Question

# Blueprintを作成
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    # データベースから最新の質問を取得
    recent_questions = Question.query.filter_by(is_deleted=False).order_by(Question.created_at.desc()).limit(10).all()
    
    return render_template('main/index.html', questions=recent_questions)

@bp.route('/about')
def about():
    """サイト紹介ページ"""
    return render_template('main/about.html')

@bp.route('/setup-db')
def setup_db():
    """データベーステーブルの作成"""
    db.create_all()
    return 'データベーステーブルが作成されました！'
