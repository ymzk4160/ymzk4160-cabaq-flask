from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
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
        {
            'id': 2,
            'title': 'お客さんとのLINE交換、みんなどうしてる？',
            'category': '営業',
            'created_at': datetime.utcnow(),
            'answer_count': 2,
            'answers': [{'content': '私はLINE交換は基本的にしないようにしています。どうしても、という場合はサブアカウントを作って、仕事用のみで使い分けています。'}]
        },
        {
            'id': 3,
            'title': '出勤日数の調整について悩んでいます',
            'category': '出勤',
            'created_at': datetime.utcnow(),
            'answer_count': 2,
            'answers': [{'content': '私も学校と両立してます！週3でも全然やっていけますよ。コツは出勤する曜日を固定することです。'}]
        },
        {
            'id': 4,
            'title': '人間関係のストレスでメンタルが限界',
            'category': 'メンタル',
            'created_at': datetime.utcnow(),
            'answer_count': 2,
            'answers': [{'content': 'すごく分かります...私も同じ経験ありました。結局私は店を変えましたが、その前に試したのは「自分の得意分野を見つけること」。'}]
        },
        {
            'id': 5,
            'title': '地元で働くのが怖い、身バレしないか心配',
            'category': '身バレ',
            'created_at': datetime.utcnow(),
            'answer_count': 2,
            'answers': [{'content': '私も地元で働いていますが、意外と知り合いに会うことは少ないです。対策としては、SNSの設定を見直す、メイクを普段と変えるなど。'}]
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
