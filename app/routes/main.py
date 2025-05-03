from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from datetime import datetime, timedelta

# Blueprintを作成
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    # 固定ダミーデータを直接作成
    now = datetime.utcnow()
    recent_questions = [
        {
            'title': '初めてのキャバクラ勤務、何から準備すれば？',
            'category': '初心者',
            'answer_count': 2,
            'answers': [{'content': 'ドレスは最初は2〜3着あれば十分です！私は最初、古着屋で手頃な値段のものを買いました。'}]
        },
        {
            'title': 'お客さんとのLINE交換、みんなどうしてる？',
            'category': '営業',
            'answer_count': 2,
            'answers': [{'content': '私はLINE交換は基本的にしないようにしています。どうしても、という場合はサブアカウントを作って、仕事用のみで使い分けています。'}]
        },
        {
            'title': '出勤日数の調整について悩んでいます',
            'category': '出勤',
            'answer_count': 2,
            'answers': [{'content': '私も学校と両立してます！週3でも全然やっていけますよ。コツは出勤する曜日を固定することです。'}]
        }
    ]
    
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
