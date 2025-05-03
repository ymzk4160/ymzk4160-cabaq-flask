from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db

# Blueprintを作成
bp = Blueprint('main', __name__)  # **name** を __name__ に修正

@bp.route('/')
def index():
    """トップページ"""
    # ダミーデータを使用して表示
    dummy_questions = [
        {
            'id': 1,
            'title': '営業についての質問1',
            'category': '営業',
            'answer_count': 3
        },
        {
            'id': 2,
            'title': '美容についての質問1',
            'category': '美容',
            'answer_count': 2
        },
        {
            'id': 3,
            'title': '恋愛についての質問1',
            'category': '恋愛',
            'answer_count': 1
        }
    ]
    
    return render_template('main/index.html', questions=dummy_questions)

@bp.route('/about')
def about():
    """サイト紹介ページ"""
    return render_template('main/about.html')

@bp.route('/setup-db')
def setup_db():
    """データベーステーブルの作成"""
    try:
        db.create_all()
        return 'データベーステーブルが作成されました！'
    except Exception as e:
        return f'エラーが発生しました: {str(e)}'

@bp.route('/seed-data')
def seed_data_route():
    return 'ダミーデータを使用中。データベース機能は現在調整中です。'
